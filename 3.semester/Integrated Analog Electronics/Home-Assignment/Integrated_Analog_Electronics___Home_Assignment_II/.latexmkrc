# Latexmk configuration for auto-sync to Obsidian

# PDF generation settings
$pdf_mode = 1;
$postscript_mode = 0;
$dvi_mode = 0;

# Run pdflatex with options
$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';

# Auto-sync to Obsidian after successful build
$success_cmd = 'bash sync_to_obsidian.sh';

# Clean up auxiliary files
$cleanup_mode = 1;
@generated_exts = qw(aux fdb_latexmk fls log out toc);

# Preview continuously (for -pvc mode)
$preview_continuous_mode = 1;
$preview_mode = 0;
