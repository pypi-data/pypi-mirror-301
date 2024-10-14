# -*- coding: UTF-8 -*-
from mgtoolbox_kernel.kernel.structure import Structure
from cavd.netio import *
from cavd.channel import Channel
from cavd.cavd_consts import LOWER_THRESHOLD
from cavd.netstorage import AtomNetwork, connection_values_list
from cavd.recovery import rediscovery_byRad_kdTree
from cavd.get_Symmetry import get_labeled_vornet
from cavd.channel_analysis import MigrationPaths
from cavd.mergecluster import load_voids_channels_from_file
from cavd.mergecluster import MergeCluster
from cavd.modules.struc_analysis import (
    get_spacegroups_number_sybol,
    get_sym_opt,
    get_radii_from_struct,
    is_ion_in_struct,
    localEnvirCom_new, 
    localEnvirCom
)



def cal_channel_merge_clusters(
    filename,
    migrant,
    ntol=0.02,
    rad_flag=True,
    lower=0,
    upper=10.0,
    rad_dict=None,
    clusterradii=0.5,
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)

    # Marking the calculated voids by Symmetry operation.
    sitesym = get_sym_opt(filename)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)
    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True, ntol)
    # add_fcs_vornet = vornet.add_facecenters(faces)
    prefixname = filename.replace(".cif", "")
    symprec = 0.01
    sym_vornet, voids = get_labeled_vornet(vornet, sitesym, symprec)
    writeNETFile(prefixname + "_origin.net", atmnet, sym_vornet)
    channels = Channel.findChannels2(vornet, atmnet, lower, upper, prefixname + ".net")
    Channel.writeToVESTA(channels, atmnet, prefixname)
    conn_val = connection_values_list(prefixname + ".resex", sym_vornet)
    voids, channels = load_voids_channels_from_file(prefixname + ".net")
    mc = MergeCluster(filename, struct, voids, channels, clusterradii=clusterradii)
    return conn_val


def outChannelToPOSCAR(
    filename, migrant, ntol=0.02, rad_flag=True, lower=0.0, upper=10.0, rad_dict=None
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)
    # Marking the calculated voids by Symmetry operation.
    sitesym = get_sym_opt(filename)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)

    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True, ntol)

    add_fcs_vornet = vornet.add_facecenters(faces)
    sym_vornet, voids = get_labeled_vornet(add_fcs_vornet, sitesym)
    prefixname = filename.replace(".cif", "")
    channels = Channel.findChannels2(
        sym_vornet, atmnet, lower, upper, prefixname + ".net"
    )

    migratPath = MigrationPaths(struct, migrant, channels)

    allPaths = migratPath.comAllPaths(prefixname)

    return allPaths


def outVesta(
    filename: str,
    migrant,
    ntol=0.02,
    rad_flag: bool = True,
    lower: float = 0.0,
    upper: float = 10.0,
    rad_dict: dict = None,
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)
    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True, ntol)
    add_fcs_vornet = vornet.add_facecenters(faces)

    # Marking the calculated voids by Symmetry operation.
    sitesym = get_sym_opt(filename)
    sym_vornet, voids = get_labeled_vornet(add_fcs_vornet, sitesym, ntol)

    prefixname = filename.replace(".cif", "")

    # calculate the connection values
    conn_val = connection_values_list(prefixname + ".resex", sym_vornet)

    channels = Channel.findChannels2(
        sym_vornet, atmnet, lower, upper, prefixname + ".net"
    )
    dims = []
    for i in channels:
        dims.append(i["dim"])
    # output vesta file for visiualization
    Channel.writeToVESTA(channels, atmnet, prefixname)

    return dims, conn_val


# The function used to calculate the ion transport descriptors.
def comDescriptors(
    filename, migrant, rad_flag=True, lower=0.0, upper=10.0, rad_dict=None, ntol=0.02
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    nei_dises = localEnvirCom_new(struct, migrant)
    symm_number, symm_sybol = get_spacegroups_number_sybol(filename)
    radii = get_radii_from_struct(struct)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)

    # Constructing a Voronoi network for given Atom network.
    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True, ntol)

    # Adding Voronoi face center into network to obatin the interstitial network.
    add_fcs_vornet = vornet.add_facecenters(faces)

    # Marking the calculated voids by Symmetry operation.
    sitesym = get_sym_opt(filename)
    sym_vornet, voids = get_labeled_vornet(add_fcs_vornet, sitesym, ntol)

    # Count the recovery rate by distance.
    voids_abs = []
    voids_rad = []
    for void in sym_vornet.nodes:
        voids_abs.append(void[2])
        voids_rad.append(void[3])

    bottlenecks = []
    bottlenecs_rad = []
    for bt in sym_vornet.edges:
        frac_bt = bt[2]
        bottlenecks.append(frac_bt)
        bottlenecs_rad.append(bt[3])

    fcens = []
    fcens_rad = []
    for fc in fcs:
        fcens.append(fc[0])
        fcens_rad.append(fc[1])

    vorosites = [voids_abs, bottlenecks, fcens]
    vororad = [voids_rad, bottlenecs_rad, fcens_rad]
    recover_rate, recover_state, migrate_mindis = rediscovery_byRad_kdTree(
        struct, migrant, vorosites, vororad
    )

    # Calculating connected threshold and dim of the interstitial network.
    prefixname = filename.replace(".cif", "")
    conn_val = connection_values_list(prefixname + ".resex", sym_vornet)
    dim_network, connect = ConnStatus(conn_val, lower, upper)

    # Calculating transport channels and dim of the transport channels.
    channels = Channel.findChannels2(
        sym_vornet, atmnet, lower, upper, prefixname + ".net"
    )
    dims_channel = []
    if len(channels) == 0:
        pass
    else:
        for i in channels:
            dims_channel.append(i["dim"])

    return (
        radii,
        symm_sybol,
        symm_number,
        nei_dises,
        conn_val,
        connect,
        dim_network,
        dims_channel,
        recover_rate,
    )


def bmd_com(
    filename, migrant, rad_flag=True, lower=0.0, upper=10.0, rad_dict=None, symprec=0.01
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    sitesym = get_sym_opt(filename)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)
    migrant_radius, migrant_alpha, nei_dises = localEnvirCom(struct, migrant)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)

    prefixname = filename.replace(".cif", "")
    # for cst paper
    # vornet,edge_centers,fcs,faces = atmnet.perform_voronoi_decomposition(True)
    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(False)
    sym_vornet, voids = get_labeled_vornet(vornet, sitesym, symprec)
    writeVaspFile(prefixname + "_origin.vasp", atmnet, sym_vornet)
    writeNETFile(prefixname + "_origin.net", atmnet, sym_vornet)
    migrate_mindis = None

    minRad = 0.0
    if lower:
        minRad = lower
    else:
        standard = LOWER_THRESHOLD[migrant]
        minRad = standard * migrant_alpha * 0.85
    conn_val = connection_values_list(prefixname + ".resex", sym_vornet)
    dim_network, connect = ConnStatus(conn_val, minRad)
    writeVaspFile(prefixname + ".vasp", atmnet, sym_vornet, minRad, upper)
    channels = Channel.findChannels2(
        sym_vornet, atmnet, lower, upper, prefixname + ".net"
    )

    # output vesta file for visiualization
    Channel.writeToVESTA(channels, atmnet, prefixname)

    dims = []
    for i in channels:
        dims.append(i["dim"])

    return radii, minRad, conn_val, connect, dim_network, dims, migrate_mindis


# Calculate interstice and bottleneck for given structure.
def bicomputation(
    filename, migrant, rad_flag=True, lower=0.0, upper=0.0, rad_dict=None
):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    sitesym = get_sym_opt(filename)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)
    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)

    prefixname = filename.replace(".cif", "")
    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True)
    add_fcs_vornet = vornet.add_facecenters(faces)
    writeVaspFile(prefixname + "_origin.vasp", atmnet, add_fcs_vornet)

    if lower and not upper:
        writeVaspFile(
            prefixname + "_selected.vasp", atmnet, add_fcs_vornet, lower, 10.0
        )
    if not lower and upper:
        writeVaspFile(prefixname + "_selected.vasp", atmnet, add_fcs_vornet, 0.0, upper)
    if lower and upper:
        writeVaspFile(
            prefixname + "_selected.vasp", atmnet, add_fcs_vornet, lower, upper
        )


# Calculate a list of connected values (Rf alongs the a, b, and c direction) for a structure.
def connValListCom(filename, migrant=None, rad_flag=True, rad_dict=None):
    struct = Structure.from_file(filename)
    is_ion_in_struct(struct, migrant)
    # sitesym = get_sym_opt(filename)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)

    atmnet = AtomNetwork.read_from_RemoveMigrantCif(filename, migrant, radii, rad_flag)

    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True)
    add_fcs_vornet = vornet.add_facecenters(faces)

    prefixname = filename.replace(".cif", "")
    conn = connection_values_list(prefixname + ".resex", add_fcs_vornet)
    return conn


# Determine the connectivity of a structure.
# According to the given radius of the target ion to determine the dimension of the interstitial network.
def connStatusCom(filename, radius, migrant=None, rad_flag=True, rad_file=None):
    connlist = connValListCom(filename, migrant, rad_flag, rad_file)
    oneD = False
    twoD = False
    threeD = False

    af = connlist[0]
    bf = connlist[1]
    cf = connlist[2]

    if radius <= af:
        aconn = True
    else:
        aconn = False

    if radius <= bf:
        bconn = True
    else:
        bconn = False

    if radius <= cf:
        cconn = True
    else:
        cconn = False

    if aconn and bconn and cconn:
        threeD = True
    if (aconn and bconn) or (aconn and cconn) or (bconn and cconn):
        twoD = True
    if aconn or bconn or cconn:
        oneD = True
    return [oneD, twoD, threeD]


# Determine the connectivity of a structure based on the list of connected values.
def ConnStatus(connlist, minRad, maxRad=10.0):
    connects = []
    for i in connlist:
        if minRad <= i and maxRad >= i:
            connects.append(True)
        else:
            connects.append(False)
    dim_net = connects.count(True)
    return dim_net, connects


# Compute the channel
def channelCom(
    filename, probe_rad=None, migrant=None, rad_flag=True, rad_dict=None, symprec=0.01
):
    struct = Structure.from_file(filename)
    sitesym = get_sym_opt(filename)
    radii = {}
    if rad_flag:
        if rad_dict:
            radii = rad_dict
        else:
            radii = get_radii_from_struct(struct)
    if migrant:
        is_ion_in_struct(struct, migrant)
        atmnet = AtomNetwork.read_from_RemoveMigrantCif(
            filename, migrant, radii, rad_flag
        )
    else:
        atmnet = AtomNetwork.read_from_CIF(filename, radii, rad_flag)

    vornet, edge_centers, fcs, faces = atmnet.perform_voronoi_decomposition(True)
    add_fcs_vornet = vornet.add_facecenters(faces)

    sym_vornet, voids = get_labeled_vornet(add_fcs_vornet, sitesym, symprec)
    prefixname = filename.replace(".cif", "")
    writeNETFile(prefixname + "_origin.net", atmnet, sym_vornet)

    channels = Channel.findChannels(sym_vornet, atmnet, probe_rad, prefixname + ".net")

    # output vesta file for visiualization
    Channel.writeToVESTA(channels, atmnet, prefixname)

    dims = []
    for i in channels:
        dims.append(i["dim"])
    return dims
