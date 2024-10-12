from aevol.models.environment import Environment
from aevol.models.individual import Individual
from aevol.models.phenotypic_function import PhenotypicFunction
from aevol.visual.utils import *


class ProteomeView:
    def draw(
        self,
        individual: Individual,
        environment: Environment,
        display_legend,
    ):
        """
        Create the "proteome" visualization

        Args:
            individual: the individual whose proteome to plot
            environment: the environment object with the phenotypic target
            display_legend: True if we want to add the legend and textual information
        """
        self.fig, self.ax = create_figure()
        self.fig.subplots_adjust(left=0.1, bottom=0.25)

        self.ax.spines["right"].set_visible(False)
        self.ax.spines["top"].set_visible(False)
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([-1, 1])

        # Draw the baseline (x = 0)
        self.ax.plot(
            [0, 1],
            [0, 0],
            color="black",
        )

        # Plot the environment gaussian curve
        self.ax.plot(
            environment.target.points["x"],
            environment.target.points["y"],
            color="blue",
            alpha=0.75,
            label="Environmental target",
        )

        # Plot the triangle corresponding to each protein
        for protein in individual.proteins:
            protein_function = PhenotypicFunction(
                [
                    [protein.m - protein.w, 0.0],
                    [protein.m, protein.h * protein.expression_level],
                    [protein.m + protein.w, 0.0],
                ]
            )

            protein_handle = self.ax.plot(
                protein_function.points["x"],
                protein_function.points["y"],
                color="black",
                alpha=0.75,
                label="" if "protein_handle" in locals() else "Proteins",
            )

        # Add a title
        plt.rcParams.update({"font.size": font_size_title})
        self.ax.set_title("Proteome of best individual", y=1, pad=5)

        # Display the legend
        if display_legend == True:
            plt.rcParams.update({"font.size": font_size_legend})
            self.ax.plot(
                [],
                [],
                " ",
                label="Number of proteins : " + str(len(individual.proteins)),
            )
            self.ax.legend(loc=(0.35, -0.3))

    def save(self, out: Path, verbose=True):
        self.fig.savefig(out)
        if verbose:
            print("Proteome view written to " + str(out))
