# --------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2024 Jayesh Badwaik <j.badwaik@fz-juelich.de>
# --------------------------------------------------------------------------------------------------

import itertools
import os
import tempfile
import shutil
import subprocess
import json
import sys
import matplotlib.pyplot
import math
import numpy


def prepare_plotting_data(experiment_array):
    complete_plotting_data = {}
    complete_plotting_data["experiment"] = []

    for experiment in experiment_array:
        plotting_data = {}
        plotting_data["pipeline"] = experiment.pipeline()
        plotting_data["workload_factor"] = float(experiment.workload_factor())
        plotting_data["runtime"] = {}
        plotting_data["runtime"]["nodes"] = []
        plotting_data["runtime"]["runtime"] = []
        for data in experiment.json_data()["data"]:
            plotting_data["runtime"]["nodes"].append(int(data["parameter"]["nodes"]))
            plotting_data["runtime"]["runtime"].append(float(data["runtime"]))

            plotting_data["runtime"]["runtime"] = [
                x
                for _, x in sorted(
                    zip(plotting_data["runtime"]["nodes"], plotting_data["runtime"]["runtime"])
                )
            ]

            plotting_data["runtime"]["nodes"] = sorted(plotting_data["runtime"]["nodes"])

        plotting_data["label"] = experiment.prefix()
        plotting_data["system"] = experiment.json_data()["experiment"]["system"]

        complete_plotting_data["experiment"].append(plotting_data)

    min_nodes = sys.maxsize
    max_nodes = 0
    min_runtime = sys.float_info.max
    max_runtime = 0

    max_workload_factor = sys.float_info.max

    for pipeline_data in complete_plotting_data["experiment"]:
        local_max = max(pipeline_data["runtime"]["nodes"])
        local_min = min(pipeline_data["runtime"]["nodes"])
        if pipeline_data["system"] == "jedi":
            factor = 1
        else:
            factor = 0.5
        min_nodes = min(min_nodes, local_min)
        max_nodes = factor * max(max_nodes, local_max)
        local_max = max(pipeline_data["runtime"]["runtime"])
        local_min = min(pipeline_data["runtime"]["runtime"])
        min_runtime = min(min_runtime, local_min)
        max_runtime = max(max_runtime, local_max)

    complete_plotting_data["node_range"] = [0.5 * min_nodes, 1.4 * max_nodes]
    complete_plotting_data["runtime_range"] = [0.5 * min_runtime, 1.4 * max_runtime]

    workload_factor_array = [
        data["workload_factor"] for data in complete_plotting_data["experiment"]
    ]
    min_workload_factor = min(workload_factor_array)
    normalized_wf = [p / min_workload_factor for p in workload_factor_array]

    for index, pipeline_data in enumerate(complete_plotting_data["experiment"]):
        pipeline_data["expected_runtime"] = {}
        pipeline_data["expected_runtime"]["nodes"] = pipeline_data["runtime"]["nodes"]
        pipeline_data["expected_runtime"]["runtime"] = [
            normalized_wf[index] * p for p in pipeline_data["runtime"]["runtime"]
        ]

    return complete_plotting_data


def generate_plot_pdf_file(plotting_data, output_dir):
    plot = matplotlib.pyplot.figure()
    marker = itertools.cycle(("o"))

    ax = plot.subplots()
    ax.set_xlabel(
        "Number of Nodes ($N_\\text{JEDI}$, $N_{4 \\mathrm{x} \\text{A100}}/2$; log-scale)"
    )
    ax.set_ylabel("Runtime / s (log-scale)")
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.margins(2)
    ax.set_xlim(plotting_data["node_range"])
    ax.set_ylim(plotting_data["runtime_range"])

    xticklabels = []
    yticklabels = []

    cmap = matplotlib.colormaps["rainbow"]

    colorgen = iter(cmap(numpy.linspace(0, 1, 2)))
    ax.grid(visible=True, which="major", axis="x", linestyle="-", linewidth=0.5, alpha=0.5)
    ax.tick_params(
        axis="both", which="minor", labelbottom=False, labelleft=False, bottom=False, left=False
    )

    jureca_data = {}
    jureca_data["nodes"] = []
    jureca_data["runtime"] = []

    jedi_data = {}
    jedi_data["nodes"] = []
    jedi_data["runtime"] = []
    for pipeline_data in plotting_data["experiment"]:
        xticklabels = xticklabels + pipeline_data["runtime"]["nodes"]
        yticklabels = yticklabels + pipeline_data["runtime"]["runtime"]
        if pipeline_data["system"] == "jedi":
            xaxis_data = pipeline_data["runtime"]["nodes"]
            yaxis_data = [p for p in pipeline_data["runtime"]["runtime"]]
            jedi_data["nodes"] = jedi_data["nodes"] + xaxis_data
            jedi_data["runtime"] = jedi_data["runtime"] + yaxis_data
        else:
            yaxis_data = [p for p in pipeline_data["runtime"]["runtime"]]
            xaxis_data = [p / 2 for p in pipeline_data["runtime"]["nodes"]]
            jureca_data["nodes"] = jureca_data["nodes"] + xaxis_data
            jureca_data["runtime"] = jureca_data["runtime"] + yaxis_data

    jureca_plot_data = {}
    jedi_plot_data = {}

    jureca_plot_data["runtime"] = [
        x for _, x in sorted(zip(jureca_data["nodes"], jureca_data["runtime"]))
    ]
    jureca_plot_data["nodes"] = sorted(jureca_data["nodes"])

    jureca_plot_data["ideal_scaling"] = [
        jureca_plot_data["runtime"][0] / p * jureca_plot_data["nodes"][0]
        for p in jureca_plot_data["nodes"]
    ]
    jureca_plot_data["low_scaling"] = [p * 1.25 for p in jureca_plot_data["ideal_scaling"]]

    jureca_color = next(colorgen)
    jedi_color = next(colorgen)

    ax.plot(
        jureca_plot_data["nodes"],
        jureca_plot_data["runtime"],
        color=jureca_color,
        label="jurecadc",
        marker=next(marker),
        markersize=4,
    )
    ax.plot(
        jureca_plot_data["nodes"],
        jureca_plot_data["ideal_scaling"],
        color=jureca_color,
        linestyle="--",
        linewidth=0.6,
        alpha=1,
    )
    ax.plot(
        jureca_plot_data["nodes"],
        jureca_plot_data["low_scaling"],
        color=jureca_color,
        linestyle="--",
        linewidth=0.6,
        alpha=1,
    )

    jedi_plot_data["runtime"] = [
        x for _, x in sorted(zip(jedi_data["nodes"], jedi_data["runtime"]))
    ]
    jedi_plot_data["nodes"] = sorted(jedi_data["nodes"])

    jedi_plot_data["ideal_scaling"] = [
        jedi_plot_data["runtime"][0] / p * jedi_plot_data["nodes"][0]
        for p in jedi_plot_data["nodes"]
    ]
    jedi_plot_data["low_scaling"] = [p * 1.25 for p in jedi_plot_data["ideal_scaling"]]

    ax.plot(
        jedi_plot_data["nodes"],
        jedi_plot_data["runtime"],
        color=jedi_color,
        label="jedi",
        marker=next(marker),
        markersize=4,
    )
    ax.plot(
        jedi_plot_data["nodes"],
        jedi_plot_data["ideal_scaling"],
        color=jedi_color,
        linestyle="--",
        linewidth=0.6,
        alpha=1,
    )
    ax.plot(
        jedi_plot_data["nodes"],
        jedi_plot_data["low_scaling"],
        color=jedi_color,
        linestyle="--",
        linewidth=0.6,
        alpha=1,
    )

    yvalues = (
        jureca_plot_data["runtime"]
        + jedi_plot_data["runtime"]
        + jureca_plot_data["low_scaling"]
        + jedi_plot_data["low_scaling"]
        + jureca_plot_data["ideal_scaling"]
        + jedi_plot_data["ideal_scaling"]
    )

    xmin = min(min(jureca_plot_data["nodes"]) / 2, min(jedi_plot_data["nodes"]))
    xmax = max(max(jureca_plot_data["nodes"]) / 2, max(jedi_plot_data["nodes"]))
    ymin = min(yvalues)
    ymax = max(yvalues)

    xticklabels = jedi_plot_data["nodes"]

    min_yticklabel = math.log(ymin * 0.5)
    max_yticklabel = math.log(ymax * 1.5)

    yticklabels = numpy.logspace(min_yticklabel, max_yticklabel, num=6, base=math.e)
    yticklabels = [int(p) for p in yticklabels]
    xticklabels = [int(p) for p in xticklabels]

    ax.set_xticks(xticklabels)
    ax.set_xticklabels(xticklabels)
    ax.set_yticks(yticklabels)
    ax.set_yticklabels(yticklabels)

    plot.legend(bbox_to_anchor=(0.5, 0.3))


    pdf_file = os.path.join(output_dir, "plot.pdf")
    png_file = os.path.join(output_dir, "plot.png")

    plot.savefig(pdf_file, bbox_inches="tight")
    plot.savefig(png_file, bbox_inches="tight")
    return "plot.pdf"


def generate_plot_tex_file(experiment_array, output_dir):
    plotting_data = prepare_plotting_data(experiment_array)
    pdf_filename = generate_plot_pdf_file(plotting_data, output_dir)

    plotfilename = os.path.join(output_dir, "plot.tex")

    with open(plotfilename, "w") as plotfile:
        plotfile.write("% This file was generated by jureap.\n")
        plotfile.write("\\exacbplot{" + pdf_filename + "}{Caption}\n")


def generate_csv_table_tex_file(experiment_array, output_dir):
    tablefilename = os.path.join(output_dir, "table.tex")
    with open(tablefilename, "w") as tablefile:
        tablefile.write("% This file was generated by jureap.\n")

        for experiment in experiment_array:
            csv_file = os.path.join(
                "data", experiment.output_pipeline_dir(), experiment.prefix() + ".csv"
            )
            tablefile.write("\\exacbtable{" + csv_file + "}{Caption}\n")


def generate_json_tex_file(experiment_array, output_dir):
    jsonfilename = os.path.join(output_dir, "json.tex")
    with open(jsonfilename, "w") as jsonfile:
        jsonfile.write("% This file was generated by jureap.\n")

        for experiment in experiment_array:
            json_file = os.path.join(
                "data", experiment.output_pipeline_dir(), experiment.prefix() + ".json"
            )
            jsonfile.write("\\lstinputlisting[caption=Caption]{" + json_file + "}\n")


def generate_author_tex_file(output_dir):
    authorfilename = os.path.join(output_dir, "author.tex")
    with open(authorfilename, "w") as authorfile:
        authorfile.write("% This file was generated by jureap.\n")
        authorfile.write("\\title{JEDI Evaluation Report}\n")


def compile_report_pdf(output_dir):
    subprocess.run(["make", "debug"], cwd=output_dir, env=os.environ)


def prepare_report_dir(output_dir, share_dir):
    texdir = os.path.join(share_dir, "jureap/tex/jedi")
    shutil.copytree(texdir, output_dir)


def write_json_data(experiment_array, output_dir):
    json_dir = os.path.join(output_dir, "json")
    os.makedirs(json_dir, exist_ok=True)
    for experiment in experiment_array:
        json_filepath = os.path.join(
            json_dir, experiment.pipeline() + "." + experiment.prefix() + ".json"
        )
        with open(json_filepath, "w") as jsonfile:
            json.dump(experiment.json_repr(), jsonfile, indent=4)


def copy_raw_data(input_dir, experiment_array, output_dir):
    data_dir = os.path.join(output_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for experiment in experiment_array:
        output_experiment_reldir = experiment.pipeline() + str(".") + experiment.prefix()
        output_experiment_dir = os.path.join(data_dir, output_experiment_reldir)
        input_experiment_dir = os.path.join(input_dir, experiment.pipeline_dir())
        csv_filepath = os.path.join(input_experiment_dir, experiment.prefix() + ".csv")
        json_filepath = os.path.join(input_experiment_dir, experiment.prefix() + ".json")
        os.makedirs(output_experiment_dir, exist_ok=True)
        shutil.copy(csv_filepath, output_experiment_dir)
        shutil.copy(json_filepath, output_experiment_dir)


def generate(input_dir, experiment_array, output_dir, share_dir, tmp_dir):
    prepare_report_dir(output_dir, share_dir)
    copy_raw_data(input_dir, experiment_array, output_dir)
    generate_plot_tex_file(experiment_array, output_dir)
    generate_csv_table_tex_file(experiment_array, output_dir)
    generate_json_tex_file(experiment_array, output_dir)
    write_json_data(experiment_array, output_dir)
    generate_author_tex_file(output_dir)
    compile_report_pdf(output_dir)
