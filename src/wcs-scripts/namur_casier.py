# Casier judiciaire.
# use-case : 595
motif1 = globals().get('form_var_selected_motifs_1')
# use-case : 596-1
motif2 = globals().get('form_var_selected_motifs_2')
# use-case : 596-2
motif3 = globals().get('form_var_selected_motifs_3')
result = str(motif1 if motif1 is not None and motif1 != 'None' else motif2 if motif2 is not None and motif2 != 'None' else motif3)
