# Reproducibility notes

## Materials and provenance

This repository contains selected weekly preparation files, plotting inputs and scripts, derived figures, and the final poster from the SURF study. The starting structure is [PDB 1Y26](https://www.rcsb.org/structure/1Y26). The original group and supervisor credits remain in the [poster](W11/poster/SURF-2025-0515-poster.pdf).

| Material | Location |
|---|---|
| Simulation setup | [W2/setup](W2/setup/) |
| Initial-frame comparison, PCA, and GROMACS hydrogen-bond map | [W5](W5/) |
| Barnaba driver, saved annotations, and base-pair analyses | [W7](W7/) |
| Main RMSD, Rg, and pairing plotting workspace | [W8/All_Plots](W8/All_Plots/) |
| Snapshot structures and PyMOL scripts | [W8/Structure_Plot/pymol](W8/Structure_Plot/pymol/) |
| RNApdbee/DSSR/VARNA-derived structure outputs | [W8/Structure_Plot/1y26_from_web](W8/Structure_Plot/1y26_from_web/) |
| Trajectory and figure preparation notes | [W8/Notes](W8/Notes/) |
| Exploratory WCc comparison | [W9/P_Value](W9/P_Value/) |
| Final figure exports and poster | [W10](W10/) · [W11](W11/) |

## Reusing the files

Run a plotting script from its own directory: the scripts generally read local XVG/CSV files and write to a sibling `img` directory. The retained folder relationships were preserved during reorganization. Some conversion scripts explicitly select one temperature; their chosen input must match the comparison being made. The saved presentation figures include later editing, so running a script alone may not reproduce every final panel exactly.

The W2 scripts and MDP files are preparation records, not a complete execution manifest for every temperature. They retain historical settings and intermediate filenames. Full TRR/XTC trajectories, binary run inputs, force-field installations, and scheduler outputs are not bundled. The topology refers to an `amber14sb_OL15.ff` installation that must be supplied for reuse. See the [original trajectory-processing notes](W8/Notes/final_trajectory_process.md) and [figure-preparation notes](W8/Notes/plots_preparation.md).

## Barnaba customization and statistics

The driver at [W7/barnaba/python/barnaba_annotate.py](W7/barnaba/python/barnaba_annotate.py) uses a local Barnaba extension named `my_dist_para_input` together with a pairing-angle cutoff. The [customization notes](W7/barnaba/barnaba.md) record the changed signatures and code; the standard [Barnaba](https://github.com/srnas/barnaba) installation alone does not provide this argument. Saved annotation filenames distinguish cutoff settings and should not be treated as interchangeable.

The W9 Welch t-test script is retained as historical exploratory code. It treats trajectory frames as independent observations; temporal autocorrelation can make its nominal p-value and confidence interval overconfident. A defensible inferential comparison would need an autocorrelation-aware analysis and appropriate independent sampling. No such reanalysis was performed for this repository.

## Scientific scope

The poster and saved numbers are historical research outputs. Later REST2/replica work and nucleotide-modification workflows belong to a separate RNA MD project. No simulations, plots, or statistical tests were rerun during repository organization.
