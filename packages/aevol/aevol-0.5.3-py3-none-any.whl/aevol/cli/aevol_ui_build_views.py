import sys
import getopt
from pathlib import Path

from aevol import __version__ as aevol_version
from aevol.visual.draw import draw_all


def main():
    """
    Create graphical views from the provided input
    """
    envfile = None
    gridfile = None
    indivfile = None
    outdir = Path(".")
    display_legend = True

    print_header()

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "e:g:hi:o:",
            ["envfile=", "gridfile=", "help", "indivfile=", "outdir="],
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        print_usage()
        sys.exit(2)
    for opt, val in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-e", "--envfile"):
            envfile = val
        elif opt in ("-g", "--gridfile"):
            gridfile = val
        elif opt in ("-i", "--indivfile"):
            indivfile = val
        elif opt in ("-o", "--outdir"):
            outdir = Path(val)
        else:
            assert False, "unhandled option"

    # Print help if nothing to do
    if gridfile is None and indivfile is None:
        print("the data you have provided is not sufficient to draw anything")
        print_usage()
        sys.exit()

    # Make sure outdir exists
    outdir.mkdir(parents=True, exist_ok=True)

    # Draw views whose required data have been provided
    draw_all(
        indivfile,
        envfile,
        gridfile,
        outdir,
        display_legend=display_legend,
        verbose=True,
    )


def print_header():
    print("aevol_ui_build_views (" + aevol_version + ") Inria - Biotic")


def print_usage():
    print(
        r"""Usage : aevol_ui_build_views -h or --help
   or : aevol_build_views [-e ENV_FILE] [-i INDIV_FILE] [-g GRID_FILE] [-o OUT_DIR]"""
    )


def print_help():
    print(
        r"""******************************************************************************
*                                                                            *
*                        aevol - Artificial Evolution                        *
*                                                                            *
* Aevol is a simulation platform that allows one to let populations of       *
* digital organisms evolve in different conditions and study experimentally  *
* the mechanisms responsible for the structuration of the genome and the     *
* transcriptome.                                                             *
*                                                                            *
******************************************************************************

aevol_ui_build_views: create graphical views from the provided input 
"""
    )
    print_usage()
    print(
        r"""
Options
  -h, --help
	print this help, then exit
  -e, --envfile ENV_FILE
	specify environment file
  -i, --indivfile INDIV_FILE
	specify individual file
  -g, --gridfile GRID_FILE
	specify grid (population) file
  -o, --outdir OUT_DIR (default: .)
	specify output directory"""
    )


if __name__ == "__main__":
    main()
