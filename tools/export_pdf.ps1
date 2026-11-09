# Export a .docx to PDF with Word (updates fields such as page numbers first).
param([Parameter(Mandatory = $true)][string]$Docx)
$Docx = (Resolve-Path $Docx).Path
$pdf = [IO.Path]::ChangeExtension($Docx, ".pdf")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($Docx)
    $doc.Fields.Update() | Out-Null
    $doc.ExportAsFixedFormat($pdf, 17)   # 17 = wdExportFormatPDF
    $doc.Close([ref]0)
} finally {
    $word.Quit()
}
Write-Output "wrote $pdf"
