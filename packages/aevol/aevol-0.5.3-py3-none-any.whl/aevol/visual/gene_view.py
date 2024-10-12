import matplotlib.pyplot as plt
from matplotlib.patches import Arc

from aevol.visual.genome_view import *
from aevol.visual.utils import *


class GeneView(GenomeView):
    def __init__(self, nb_layers=max_layers):
        GenomeView.__init__(self, nb_layers)

    def draw(self, individual, display_legend):
        """
        Create the "gene" visualization

        Args:
            individual: the individual object with all the information to plot the graph
            display_legend: True if we want to add the legend and textual information
        """
        # For each protein (that contains the data of the corresponding gene)
        for protein in individual.proteins:
            self.draw_gene(protein, individual.genome_length)

        del self.occupied_sectors

        # Add the subplot title
        plt.rcParams.update({"font.size": font_size_title})
        self.ax.set_title("Genome and genes", y=1.0, pad=5)

        # Display the legend
        if display_legend == True:
            plt.rcParams.update({"font.size": font_size_legend})
            self.ax.legend(
                [],
                [],
                title="Genome length : "
                + str(individual.genome_length)
                + " bp"
                + "\nNumber of genes : "
                + str(len(individual.proteins)),
                loc=(0.85, 0),
            )

    def draw_gene(self, gene, genome_length):
        """
        Draw the provided gene on the figure.

        Args:
            gene: the gene to be drawn
            genome_length:
        """
        diameter = 2 * radius

        # Compute the angles of the ROI on the genome circle
        begin_angle, end_angle = gene.compute_angles(genome_length)

        # Compute the layer of the ROI (the distance from the genome circle)
        try:
            layer = self.compute_layer(gene.strand, begin_angle, end_angle)
        except Exception as e:
            print(e)
            return
        offset = layer * delta

        # Compute the display color of the ROI
        color = "black"

        # We add 0.15 to the strand angles for visibility
        if gene.strand == "LEADING":
            self.ax.add_patch(
                Arc(
                    center,
                    diameter + offset,
                    diameter + offset,
                    angle=90,
                    theta1=-end_angle - 0.15,
                    theta2=-begin_angle + 0.15,
                    linewidth=6,
                    color=color,
                )
            )
        else:
            self.ax.add_patch(
                Arc(
                    center,
                    diameter + offset,
                    diameter + offset,
                    angle=90,
                    theta1=-begin_angle - 0.15,
                    theta2=-end_angle + 0.15,
                    linewidth=6,
                    color=color,
                )
            )

    def save(self, out: Path, verbose=True):
        self.fig.savefig(out)
        if verbose:
            print("Gene view written to " + str(out))
