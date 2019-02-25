from matplotlib import pyplot as plt

from graph import my_graph_helpers as mgh

"""
This example file demonstrates how to import a shapefile, finding and
 plotting the shortest distance of roads necessary to achieve universal road
 access for all parcels.

The shortest distance of roads algorithm is based on probablistic greedy search
so different runs will give slightly different answers.

 """


def new_import(filename, name=None, byblock=True, threshold=1):
    """ imports the file, plots the original map, and returns
    a list of blocks from the original map.
    """

    if name is None:
        name = filename

    original = mgh.import_and_setup(filename,
                                    threshold=threshold,
                                    byblock=byblock,
                                    name=name)

    blocklist = original.connected_components()

    plt.figure()
    # plot the full original map
    for b in blocklist:
        # defines original geometry as a side effect,
        b.plot_roads(master=b, new_plot=False, update=True)

    blocklist.sort(key=lambda b: len(b.interior_parcels), reverse=True)

    return blocklist


def run_once(blocklist):

    """Given a list of blocks, builds roads to connect all interior parcels and
    plots all blocks in the same figure.
    """

    map_roads = 0
    plt.figure()

    for original in blocklist:
        original.define_roads()
        original.define_interior_parcels()
        if len(original.interior_parcels) > 0:
            block = original.copy()

            # define interior parcels in the block based on existing roads
            block.define_interior_parcels()

            # finds roads to connect all interior parcels for a given block
            block_roads = mgh.build_all_roads(block, wholepath=True)
            map_roads = map_roads + block_roads
        else:
            block = original.copy()

        block.plot_roads(master=original, new_plot=False)

    return map_roads


def main(filename, name, byblock, threshold):
    blocklist = new_import(filename, name, byblock=byblock, threshold=threshold)
    geojson = blocklist[0].myedges_geoJSON()
    map_roads = run_once(blocklist)

    plt.show()

    return (blocklist, geojson, map_roads)

if __name__ == "__main__":
    # SINGLE SMALL BLOCK
    # main(
    #     filename  = "data/epworth_demo", 
    #     name      = "ep single",
    #     byblock   = True,
    #     threshold = 0.5)

    # MANY SMALL BLOCKS, epworth
    # some of the blocks here require a threshold of 0.5
    # main(
    #     filename  = "data/epworth_before",
    #     name      = "ep many",
    #     byblock   = True,
    #     threshold = 0.5)

    # MANY SMALL BLOCKS, Phule Nagar
    # some of the blocks here require a threshold of 0.5
    main(
        filename  = "data/phule_nagar_v6",
        name      = "phule",
        byblock   = False,
        threshold = 0.5)

    # ONE LARGE BLOCK
    # main(
    #     filename = "data/capetown",
    #     name = "cape",
    #     byblock = False,
    #     threshold = 1)


