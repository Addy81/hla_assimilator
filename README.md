# HLA Assimilator

High resolution HLA typing information is required as an input for algorithms used to determine immunogenicity scores (Kosmoliaptsis et al., Transplantation 2009, 88). Undertaking high resolution HLA typing on retrospective cohorts of solid organ transplant patients is both time consuming and expensive. Therefore, we sought to develop an algorithm that could be used to convert existing low/intermediate resolution HLA typing information into high resolution data, which would then be used to generate immunogenicity scores.

Our tool manipulates low resolution data and transforms them into high resolution hla information based on 132 assimilation rules derived from literature and web databases (allelefrequencies.net & haplostats.org)

## Getting Started

The only thing you need to run the tool is the assimilator.py script found in bin/

```
python bin/assimilator.py -h
usage: assimilator.py [-h] [-o OUTPUT] input

Assimilate low resolution HLA type data.

positional arguments:
  input                 Input excel .xlsx to be analysed

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Desired output name filename to be

```


### Prerequisites

```
The pandas python package is required. 

$ pip install pandas

```

### Required Input

The script works on xlsx speadsheets, it recognises specified columns based on the Addenbrooke's Tissue Typing Deparment NGS output, manipulates existing data, adds it to new columns and outputs an updated spreadsheet.


If you want to try it, the script requires the following header: [header.txt](header.txt)



## Authors

* **Adriana Toutoudaki** - *Computational Work*
* **Hannah Turnbull** - *Association table creation*


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This project was undertaken as part of research project for the Clinical Science Master's Programme at the University of Manchester as part of the Scientist Training Programme requirements, under the supervision of:

* **Sarah Peacock** - *Lab Director; Tissue Typing Department*
* **Vassilis Kosmoliaptsis** - *Transplant Surgeon*
* **Matthew Garner** - *Bioinformatician*



## Disclaimer

The program is distributed in the hope that it will be useful, but without any warranty. It is provided "as is" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose. The entire risk as to the quality and performance of the program is with you. Should the program prove defective, you assume the cost of all necessary servicing, repair or correction.									
									
In no event unless required by applicable law the author will be liable to you for damages, including any general, special, incidental or consequential damages arising out of the use or inability to use the program (including but not limited to loss of data or data being rendered inaccurate or losses sustained by you or third parties or a failure of the program to operate with any other programs), even if the author has been advised of the possibility of such damages.									







