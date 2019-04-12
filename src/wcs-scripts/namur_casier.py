# Casier judiciaire.
raison = globals().get('form_var_raison_demande') or ''
motif = ''
if '595' in raison:
    motif = globals().get('form_var_selected_motifs_1')
if '596-1' in raison:
    motif = globals().get('form_var_selected_motifs_2')
if '596-2' in raison:
    motif = globals().get('form_var_selected_motifs_3')

result = str(motif)
