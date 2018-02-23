# Casier judiciaire.
motif1 = globals().get('form_var_selected_motifs_1')
motif2 = globals().get('form_var_selected_motifs_2')
result = str(motif1 if motif1 is not None and motif1 != 'None' else motif2)
