
import re
import os
import csv
import sys
import glob
import pickle
from ggpy.utils import (fas_to_dic,
                        export_fasta, 
                        runshell, 
                        remove_files, 
                        codon_partitions, 
                        close_gaps)

myos = sys.platform

if myos == 'darwin':
    RAXML = 'raxmlHPC-PTHREADS-SSE3_Darwin_64bit'

elif myos == 'linux' or  myos == 'linux2':
    RAXML = 'raxmlHPC-PTHREADS-SSE3_Linux_64bit'


SEQMT   = "seqmt"
MAKERMT = "makermt"
CONSEL  = "consel"
CATPV   = "catpv"
FLAGMODELS = ['JC69', 'HKY85', 'K80']
class Consel:

    def __init__(self, 
                 raxml_exe   = RAXML,
                 evomodel    = 'GTRGAMMA',
                 seqmt_exe   = SEQMT,
                 makermt_exe = MAKERMT,
                 consel_exe  = CONSEL,
                 catpv_exe   = CATPV,
                 codon_partition = True, 
                 out_report = "au_tests.csv",
                 threads     = 1,
                 parallel_gt = False,
                 ):


        self.out_report  = out_report

        self.raxml_exe   = raxml_exe
        self.seqmt_exe   = seqmt_exe
        self.makermt_exe = makermt_exe
        self.consel_exe  = consel_exe
        self.catpv_exe   = catpv_exe

        self.codon_partition = codon_partition
        self.threads  = threads
        self.parallel_gt = parallel_gt
        self.evomodel = evomodel

    @property
    def _adj_threads(self):
        return self.threads if self.parallel_gt else 1

    def remove_undetermined_chars(self, seq_file: str, outname: str) -> None:
        """
        RAxML does not allow to have site likehoods for sites 
        without data. Sites completely empty are posible when
        codon-based alignment are performed as only one position
        out of three could be recovered from given sequences.
        """
        in_aln  = fas_to_dic(seq_file)
        out_aln = close_gaps(in_aln, is_codon_aware=False, model=self.evomodel) # is_codon_aware=False: check column-by-column
        export_fasta(aln = out_aln, outname=outname)

    def _site_likehood(self, seq_tree_treeID, suffix, error_file):
        """
        Site likelihoods are estimated without accounting
        for codon partitions because:         \\
        i)  Empty sites precludes estimations \\
        ii) The signal of the change when comparing site 
            likelihood using different trees should be 
            recovered because all estimations for the same site
            use the same Q matrix. Then, the signal of change 
            for a site should be present by using either Q matrix 1 
            or Q matrix 2, and so on.
            
        :returns: |str| site_llh_out 
        """

        seq,tree_nHypos,tree_id = seq_tree_treeID
        # seq,tree_nHypos = (aln_f, whole_constrs_f)
        # suffix = self.suffix
        seq_basename    = os.path.basename(seq)
        tree_basename   = os.path.basename(tree_nHypos)


        site_lnl_out_suffix = tree_basename + ".sitelh"
        seq_gap_close  =  "%s_%s_close.fasta" % (seq_basename, suffix)
        std_err_holder = tree_basename + ".stdout"
        info_carrier   = "RAxML_info." + site_lnl_out_suffix
        site_lnl_out   = "RAxML_perSiteLLs." + site_lnl_out_suffix

        # gaps are closed
        self.remove_undetermined_chars(seq, seq_gap_close)

        cmd = """
            {raxml}\
                -f g\
                -s {seq}  \
                -p 12038\
                -m {model}\
                -z {constr}\
                -n {suffix}\
                -T {threads}""".format(
                    raxml   = self.raxml_exe,
                    model   = 'GTRGAMMA' if self.evomodel in FLAGMODELS else self.evomodel,
                    seq     = seq_gap_close,
                    constr  = tree_nHypos,
                    threads = self._adj_threads,
                    suffix  = site_lnl_out_suffix).strip()
        
        if self.evomodel in FLAGMODELS:
            cmd += f" --{self.evomodel}"

        # print(cmd)
        runshell( (cmd.split(), std_err_holder), type = "stdout")
        remove_files([ 
            std_err_holder, 
            info_carrier, 
            seq_gap_close,
            seq_gap_close + ".reduced",
            # tree_nHypos
        ])

        is_there_out = os.path.isfile(site_lnl_out)

        if not is_there_out:
            with open(error_file, 'a') as f:
                writer = csv.writer(f, delimiter = "\t")
                writer.writerows([[ seq_basename, 'SLL', tree_id]])

            print( "\nError: Estimation of SLL from '%s' using '%s' hypothesis failed\n" % (seq_basename, tree_id) )
            raise Exception("Estimation of SLL failed")

        else:
            return site_lnl_out

    def _site_likehood_iter(self, seq_tree_list):
        for seq_tree in seq_tree_list:
            self._site_likehood(seq_tree)

    def _is_incongruent(self, table):
        rank = '1'

        is_congruent   = table[rank]['item'] == '1'
        is_significant = float(table[rank]['au']) >= 0.95

        if not is_congruent and is_significant:
            return True

        else:
            return False

    def au_table(self, consel_out):
        '''
        # rank, item, au

        Example of consel out (withour initial apostrophes):
        '# reading RAxML_perSiteLLs.E1381.fasta_Two_Hypothesis.pv\\
        '# rank item    obs     au     np |     bp     pp     kh     sh    wkh    wsh |\\
        '#    1    1   -4.7  0.932  0.899 |  0.897  0.991  0.886  0.886  0.886  0.886 |\\
        '#    2    2    4.7  0.068  0.101 |  0.103  0.009  0.114  0.114  0.114  0.114 |\\       
        '''
        # table = {}
        table = []
        with open(consel_out, 'r') as f:
            for i in f.readlines():
                line = i.strip()
                if line and not re.findall("(rank|reading)", line):
                    columns = re.split("[ ]+", line)
                    # rank, item, au
                    table.append([ columns[1], columns[2], columns[4] ])
        return table
        
    def _consel_pipe(self, seq_basename, siteout, error_file):
        """
        # rank, item, au
        """
        # seq, siteout, error_file = aln_f, sll_f, self.unable_to_run_f
        # seq_basename = os.path.basename(seq)
        
        # avoid conflict with consel
        # extension processor
        new_name_siteout = siteout.replace(".", "_").replace("_sitelh", ".sitelh")
        if not os.path.isfile(new_name_siteout):
            os.rename(siteout, new_name_siteout)


        in_noExtension = new_name_siteout.replace(".sitelh", "")
        to_parse_table = in_noExtension + ".out"
        msg_holder     = in_noExtension + ".ignore"
        pvalue_file    = in_noExtension + ".pv"

        seqmt_cmd   = "%s --puzzle %s" % (self.seqmt_exe, in_noExtension)
        makermt_cmd = "%s %s" % (self.makermt_exe, in_noExtension)
        consel_cmd  = "%s %s" % (self.consel_exe, in_noExtension)
        catpv_cmd   = "%s %s" % (self.catpv_exe, in_noExtension)

        runshell( (seqmt_cmd.split(),   msg_holder), type = "stdout" )
        runshell( (makermt_cmd.split(), msg_holder), type = "stdout" )
        runshell( (consel_cmd.split(),  msg_holder), type = "stdout" )

        is_there_pv = os.path.isfile(pvalue_file)

        if not is_there_pv:
            with open(error_file, 'a') as f:
                writer = csv.writer(f, delimiter = "\t")
                writer.writerows([[ seq_basename, 'consel', '']])

            out_table = None
        else:

            runshell( (catpv_cmd.split(), to_parse_table), type = "stdout" )            
            out_table = self.au_table(to_parse_table) 

        remove_files([
            new_name_siteout,
            in_noExtension + ".mt",
            in_noExtension + ".vt",
            in_noExtension + ".rmt",
            in_noExtension + ".pv",
            in_noExtension + ".ci",
            in_noExtension + ".ignore",
            to_parse_table
        ])

        return out_table

class Raxml:
    def __init__(self, 
                raxml_exe = RAXML,
                evomodel = None,
                iterations = None,
                codon_partition = None,
                threads = 1,
                paralell_gt = False,
                ):

        self.raxml_exe = raxml_exe
        self.evomodel = evomodel
        self.iterations = iterations
        self.codon_partition = codon_partition
        self.threads = threads
        self.parallel_gt = paralell_gt

    @property
    def _adj_threads(self):
        return self.threads if self.parallel_gt else 1 

    def __remove_raxmlfs__(self, seq, seq_basename):

        remove_files(
            [   seq,
                seq + ".reduced", 
                seq + "_constr.tree", 
                seq + ".stdout",
                seq + ".partitions",
                seq + ".partitions.reduced"
             ]  + \
            glob.glob( "RAxML_log."    + seq_basename + "*" ) +\
            glob.glob( "RAxML_result." + seq_basename + "*" ) +\
            glob.glob( "RAxML_info."   + seq_basename + "*" )
        )

    def __save_obj__(self, obj = None, name = None):

        with open( name , 'wb') as f:
            pickle.dump(obj, f, pickle.DEFAULT_PROTOCOL)

    def __load_info__(self, name = None):

        with open( name, 'rb') as f:
            return pickle.load(f)

    def __iter_raxml__(self, pr_message, error_file, run_id):
        """
        raxml iterator
        """
        cons_message = {}

        seq = next(iter(pr_message.values()))['aln']
        seq_basename = os.path.basename(seq)

        for pr_id in sorted(pr_message.keys()):
            # pr_id,metadata
            metadata   = pr_message[pr_id]
            pruned_str = metadata['pruned']

            seq2   = "%s_H%s_%s" % (seq, pr_id, run_id)
            pruned = seq2 + "_constr.tree"

            seq2_basename = os.path.basename(seq2)
            suffix        = seq2_basename + ".tree"
            final_out     = "RAxML_bestTree." + suffix
            

            with open( seq, 'r' ) as f:
                with open( seq2, "w" ) as f2:
                    f2.writelines( f.readlines() )

            with open(pruned, 'w') as f:
                f.write(pruned_str)
      
            if self.codon_partition:
                    part_out      = seq2 + ".partitions"
                    partition_cmd = "-q %s" % part_out
                    codon_partitions(file = seq2, outname = part_out)

            else:
                partition_cmd = ""

            cmd = """
                {raxml}         \
                    -p 12038    \
                    -g {pruned} \
                    -m {model}  \
                    -s {seq}    \
                    {partitions}\
                    -n {suffix} \
                    --silent    \
                    -N {runs}\
                    -T {threads}""".format(
                        raxml      = self.raxml_exe,
                        pruned     = pruned,
                        model      = 'GTRGAMMA' if self.evomodel in FLAGMODELS else self.evomodel,
                        seq        = seq2,
                        partitions = partition_cmd,
                        suffix     = suffix,
                        runs       = self.iterations,
                        threads    = self._adj_threads
                    ).strip()
            
            if self.evomodel in FLAGMODELS:
                cmd += f" --{self.evomodel}"
            # print(cmd)
            runshell( ( cmd.split(), seq2 + ".stdout" ), type = "stdout" )

            self.__remove_raxmlfs__(seq2, seq2_basename)

            is_there_out = os.path.isfile(final_out)
            
            if not is_there_out:
                with open(error_file, "a") as f:
                    writer = csv.writer(f, delimiter = "\t")
                    writer.writerows([[ seq_basename, 'Constraint', pr_id ]])

                print("\nError: Constraint of '%s' using '%s' hypothesis failed\n" % ( seq_basename, pr_id ) )
                raise Exception("Constraint failed")
            
            cons_message[pr_id] = {
                    'group'       : metadata['group'],
                    'aln'         : metadata['aln'],
                    'constrained' : final_out
                }

        return cons_message


