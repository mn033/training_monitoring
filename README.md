# Training Monitoring for climbers
This is a small command line tool, which visualizes climbing training statistics. This little command line tool 
reads a .xls-file, which is specified by '<--input /path/to/xlsfile>' and generates a PDF or SVG. 
The .xls-file has to be in a certain form (see ...link...). 

Charts and graphs are built by the help of matplotlib. The visualization of the training data should help 
keeping track of the invested effort, seeing correlations and analyzing for improvements.
![Sample plot](res/sample_fig.svg?raw=true)
## To-Do
- [ ] support of Google Spreadsheets
- [ ] improvement of PDF rendering
- [ ] improvement of the plotting
- [ ] fine tuning of captured training data (maybe it should be extended by HRV, food intake, etc...)
