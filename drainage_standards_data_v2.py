# -*- coding: utf-8 -*-
"""
TXDOT CULVERT AND DRAINAGE STANDARDS MASTER REPOSITORY - PART 1 OF 4
Items 1 through 28: Bridge Rail Anchorage, Installation, and Precast Inlets & Manholes

line 277
TXDOT CULVERT AND DRAINAGE STANDARDS MASTER REPOSITORY - PART 2 OF 4
Items 29 through 56: Pipe Safety End Treatments & Early Multi-Box Culverts

line 514
TXDOT CULVERT AND DRAINAGE STANDARDS MASTER REPOSITORY - PART 3 OF 4
Items 57 through 84: Large Multi-Box Culverts, Cast-In-Place Box Culverts (XBC), and Headwalls (CH)

line 783
TXDOT CULVERT AND DRAINAGE STANDARDS MASTER REPOSITORY - PART 4 OF 4
Items 85 through 113: Riprap, Underdrains, Retaining Wall Drainage, Gates, Trash Racks, and Detour Standards




"""

TXDOT_DRAINAGE_STANDARDS = [
    {
        "code": "CD-T631-CM-20",
        "category": "Bridge Rail Anchorage",
        "title": "Mounting Details for T631 & T631LS Rails",
        "summary": "This standard provides comprehensive mounting details for T631 and T631LS traffic rails on drainage structures. It outlines concrete thickness requirements ranging from a minimum structural slab thickness of 8 inches up to 12 inches under anchor zones. Engineers must carefully evaluate the connection reinforcement steel spacing, embedment length, and baseplate tolerances. Proper anchorage requires inspecting bolt embedment and specified epoxy or cast-in-place insert options to prevent pullout under impact loads. End treatments and transition connections must interface seamlessly with adjacent bridge railing standards. Reviewers are encouraged to cross-reference related barrier and box culvert rail mounting details such as CD-RAC-20 to ensure load path continuity.",
        "constraints": "Structural slab thickness: 8\" min to 12\" max | Anchor embedment requirements",
        "file_name": "CD-T631-CM-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-T631-CM-20.pdf"
    },
    {
        "code": "CD-RAC-R-20",
        "category": "Bridge Rail Anchorage",
        "title": "Retro Guide for Box Culverts with Curbs 2 ft & less",
        "summary": "This standard establishes the retrofit guidelines for mounting protective traffic rails on existing box culverts featuring curb heights of 2 feet or less. The standard specifies minimum concrete overlay and slab strengthening thickness requirements starting at 6 inches to accommodate new anchor loads. Design engineers must examine existing field conditions, concrete cover depths, and existing rebar interference before detailing connection dowels. Connection details mandate epoxy-grouted reinforcing bars with strict minimum embedment depths to achieve composite structural behavior. Appropriate end treatments and transition wingwall connections must be checked for structural adequacy. Engineers should also evaluate companion standards like CD-SETBR-20 for comprehensive culvert retrofitting solutions.",
        "constraints": "Existing curb height <= 2 ft | Min strengthening slab thickness: 6\"",
        "file_name": "CD-RAC-R-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-RAC-R-20.pdf"
    },
    {
        "code": "CD-RAC-20",
        "category": "Bridge Rail Anchorage",
        "title": "Box Culvert Rail Mounting Details",
        "summary": "This document specifies standard mounting configurations for traffic rails directly placed over new cast-in-place and precast box culvert top slabs. The minimum top slab thickness must satisfy a structural threshold of 8.5 inches to properly anchor the railing posts under collision forces. Engineers must review the transverse distribution reinforcement and locate blockouts or preformed holes precisely according to plan dimensions. Connection joints require specific joint sealing materials and continuous longitudinal tie beams to distribute impact forces across multiple barrel sections. End treatments must coordinate with standard safety end treatments or wingwalls. Designers should verify compatibility with CD-XBC standards and related barrier connection drawings.",
        "constraints": "Top slab thickness: 8.5\" min | Transverse distribution reinforcement required",
        "file_name": "CD-RAC-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-RAC-20.pdf"
    },
    {
        "code": "CD-TPI-24",
        "category": "Pipe Installation",
        "title": "Thermoplastic Pipe Installation",
        "summary": "This standard details the bedding, backfill, and structural trench requirements for thermoplastic pipe installations under roadway embankments. Minimum cover requirements range from 1.0 foot to deep burial limits depending on pipe stiffness, while trench wall thickness and embedment material gradation are strictly enforced. Engineers must examine pipe-soil interaction parameters, deflection limits, and select backfill compaction levels achieving 95 percent standard Proctor density. Connection joints require gasketed bell-and-spigot or split-coupling systems to maintain soil-tight or water-tight integrity. End treatments must utilize appropriate pipe safety end treatments or concrete headwalls. Designers should compare these requirements with flexible metal pipe standards and CD-GSES installation guides.",
        "constraints": "Cover height: 1.0 ft min | Backfill compaction: 95% Proctor density",
        "file_name": "CD-TPI-24.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-TPI-24.pdf"
    },
    {
        "code": "CD-PAZD-CZ-20",
        "category": "Inlets & Drains",
        "title": "Precast Area Zone Drain within Clear Zone",
        "summary": "This drawing outlines precast area zone drain configurations specifically modified for safe deployment within the roadway clear zone. The design features a flush, traffic-rated structural grate and heavy-duty precast body walls with a minimum thickness of 5 inches. Engineers must verify hydraulic interception capacity, local depression grading, and subsurface connection pipe alignments. Connection details specify resilient connectors or grouted annular spaces to prevent differential settlement between the drain body and incoming pipes. End treatments and frame-grate flushness criteria are critical to prevent vehicle snagging hazards. Engineers should cross-reference standard area drains like CD-PAZD-20 and median barrier drainage details.",
        "constraints": "Wall thickness: 5\" min | Clear zone flush-mount grate requirements",
        "file_name": "CD-PAZD-CZ-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PAZD-CZ-20.pdf"
    },
    {
        "code": "CD-PAZD-20",
        "category": "Inlets & Drains",
        "title": "Precast Area Zone Drain",
        "summary": "This standard details standard precast area zone drains utilized for collection of surface runoff in ditch bottoms and median areas outside primary traffic lanes. The precast concrete structure features wall thicknesses varying from 4.5 inches to 6 inches for structural stability under lateral soil pressures. Designers must check inlet sizing, grate open area ratios, and anticipated debris loading. Pipe connections require flexible boot connectors or non-shrink grout seals to accommodate minor ground movements without cracking. Outlets should connect directly to downstream storm sewer lines or junction boxes. Engineers should review CD-PAZD-CZ-20 when positioning similar units near travel lanes.",
        "constraints": "Wall thickness: 4.5\" to 6\" | Flexible boot or grouted pipe connections",
        "file_name": "CD-PAZD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PAZD-20.pdf"
    },
    {
        "code": "CD-PMBD-20",
        "category": "Inlets & Drains",
        "title": "Precast Median Barrier Drain",
        "summary": "This standard provides precast concrete details for drainage inlets integrated directly beneath or adjacent to highway median barrier systems. The structural shell requires a minimum wall and slab thickness of 6 inches to withstand heavy wheel load impacts and lateral earth pressures. Engineers must review internal flow channels, cleanout access ports, and high-capacity slotted top inlets. Connections to longitudinal underdrains or trunk storm sewers require robust watertight joints with rubber gaskets. End transitions must match standard median barrier profiles without creating abrupt geometric offsets. Designers should examine CD-POD-20 and CD-PMBD standards for complete highway drainage continuity.",
        "constraints": "Wall/Slab thickness: 6\" min | Watertight rubber gasket joint connections",
        "file_name": "CD-PMBD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PMBD-20.pdf"
    },
    {
        "code": "CD-POD-20",
        "category": "Inlets & Drains",
        "title": "Precast Overpass Drain",
        "summary": "This standard details precast overpass drainage units designed to capture bridge deck and elevated roadway runoff efficiently. The precast structure requires minimum concrete thicknesses of 6 inches for structural base slabs and catch basins. Design engineers must calculate accurate deck drainage capture volumes and verify downspout drop pipe alignments. Connection details involve flanged or banded heavy-duty connections secured with stainless steel hardware to resist vibrational fatigue. Discharge routing connects into bridge drainage manifolds or column-concealed storm pipes. Engineers should cross-reference CD-BD series bridge drains and CD-PMBD for comprehensive bridge and overpass hydrology coordination.",
        "constraints": "Base/Wall thickness: 6\" min | Heavy-duty flanged and banded connections",
        "file_name": "CD-POD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-POD-20.pdf"
    },
    {
        "code": "CD-EX-PSL-20",
        "category": "Precast Inlets & Manholes",
        "title": "Example of PSL Styles and Sizes",
        "summary": "This reference sheet supplies design calculation examples and sizing selection charts for Precast Slab Lid (PSL) applications. It details slab thicknesses ranging from 8 inches to 12 inches depending on AASHTO HL-93 live loading and earth cover depths up to 15 feet. Engineers must evaluate opening dimensions, reinforcement steel placement schedules, and manhole collar clearances. Connection details between the precast slab lid and underlying riser sections require specialized beddings and leveling grout pads. End configurations and access hatch provisions must align with site safety standards. Designers must use this sheet alongside CD-PSL-20 for final drawing production.",
        "constraints": "Slab thickness: 8\" to 12\" | HL-93 live load and cover height schedules",
        "file_name": "CD-EX-PSL-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-EX-PSL-20.pdf"
    },
    {
        "code": "CD-PSL-20",
        "category": "Precast Inlets & Manholes",
        "title": "Precast Slab Lid",
        "summary": "This standard specifies structural fabrication and reinforcement details for standard precast concrete slab lids used across manholes and junction boxes. The precast slab thickness is standardized at a minimum of 8 inches for standard highway wheel loads. Design engineers must verify clear opening cutouts, eccentric collar options, and lifting insert specifications. Connection details require non-shrink grout placement in the keyway joint between the lid and riser walls to ensure shear transfer. Surface slopes and drainage profiles on top of the lid must prevent ponding. Engineers should consult CD-EX-PSL-20 and precast base standards like CD-PB-20 during layout.",
        "constraints": "Standard slab thickness: 8\" min | Keyway shear joint connection",
        "file_name": "CD-PSL-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSL-20.pdf"
    },
    {
        "code": "CD-CGT-PCU-23",
        "category": "Inlets & Drains",
        "title": "Curb & Gutter Transition Details for PCU Inlet",
        "summary": "This standard details the geometric curb and gutter transition profiles required for Precast Curb Inlet Under Roadway (PCU) installations. Concrete thickness for the transition apron matches standard roadway gutter depths at a minimum of 6 inches. Engineers must examine gutter depression slopes, flowline transitions, and catch basin opening geometry to maximize capture efficiency. Connection details require smooth dowelled joints or monolithic pours tying into adjacent roadway pavement sections. Surface drainage continuity must be verified to prevent bypass flow across intersections. Designers should review CD-PCU-23 and CD-CGT-PCO-23 for complete inlet transition consistency.",
        "constraints": "Apron/Gutter thickness: 6\" min | Flowline transition grading requirements",
        "file_name": "CD-CGT-PCU-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CGT-PCU-23.pdf"
    },
    {
        "code": "CD-PCU-23",
        "category": "Inlets & Drains",
        "title": "Precast Curb Inlet Under Roadway",
        "summary": "This standard presents structural and geometric details for precast curb inlets positioned directly underneath traffic lanes. The precast box walls and top slabs require robust concrete thicknesses ranging from 6 inches to 8 inches to withstand heavy traffic loads. Engineers must verify structural capacity under HL-93 live loading and check internal hydraulic drop characteristics. Connection details specify interlocking tongue-and-groove joints sealed with mastic or rubber gaskets, along with grouted pipe knockouts. Inlet throat openings and frame elevations must match pavement cross-slopes. Designers should cross-reference CD-CGT-PCU-23 and CD-PCO-23 for outside-roadway alternatives.",
        "constraints": "Wall/Slab thickness: 6\" to 8\" | HL-93 live loading | Tongue-and-groove joints",
        "file_name": "CD-PCU-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PCU-23.pdf"
    },
    {
        "code": "CD-CGT-PCO-23",
        "category": "Inlets & Drains",
        "title": "Curb & Gutter Transition Details for PCO Inlet",
        "summary": "This standard defines transition grading and concrete geometry for curb and gutter systems approaching Precast Curb Inlets Outside Roadway (PCO). Minimum concrete thickness for aprons and transition slabs is 6 inches. Engineers must review gutter depression slopes, transition lengths, and depressed curb heights to ensure optimal hydraulic interception without creating vehicle bumping hazards. Connection details dictate dowelled construction joints tied into existing or proposed curb lines. Surface drainage profiles must direct all gutter flow directly into the throat opening. Engineers should pair this standard with CD-PCO-23 and CD-CGT-PCU-23.",
        "constraints": "Transition thickness: 6\" min | Gutter depression and dowelled construction joints",
        "file_name": "CD-CGT-PCO-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CGT-PCO-23.pdf"
    },
    {
        "code": "CD-PCO-23",
        "category": "Inlets & Drains",
        "title": "Precast Curb Inlet Outside Roadway",
        "summary": "This drawing outlines specifications for precast curb inlets located outside primary travel lanes, typically in shoulder or grass median areas. Structural wall and slab thicknesses are maintained at a minimum of 6 inches. Engineers must check earth cover loads, lateral soil pressures, and riser section heights. Connection details feature standard precast joint seals and flexible pipe penetrations for incoming storm sewer lines. Outlet pipes require secure grouted connections and appropriate headwall or wingwall end treatments. Designers should cross-reference CD-PCU-23 for under-roadway versions and CD-CGT-PCO-23 for curb transitions.",
        "constraints": "Wall/Slab thickness: 6\" min | Flexible pipe penetrations and joint seals",
        "file_name": "CD-PCO-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PCO-23.pdf"
    },
    {
        "code": "CD-PRM-23",
        "category": "Precast Inlets & Manholes",
        "title": "Precast Round Manhole",
        "summary": "This standard provides precast concrete details for round manhole structures used in deep storm sewer networks. Wall thicknesses vary by manhole diameter, starting at a minimum of 5 inches for 48-inch diameter units up to 8 inches for larger diameters. Design engineers must evaluate groundwater hydrostatic uplift pressures, structural wall strength, and vertical load capacities. Connection details mandate resilient rubber O-ring or mastic joints between riser rings and base sections, combined with core-drilled or cast-in pipe boots. Top openings require adapter rings and heavy-duty manhole covers. Engineers should review CD-PJB-20 and CD-PB-20 for box-shaped drainage structure alternatives.",
        "constraints": "Wall thickness: 5\" to 8\" min based on diameter | Rubber O-ring joints",
        "file_name": "CD-PRM-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PRM-23.pdf"
    },
    {
        "code": "CD-PDD-20",
        "category": "Precast Inlets & Manholes",
        "title": "Design Data for PB and PJB",
        "summary": "This standard supplies comprehensive engineering design tables and sizing data for Precast Bases (PB) and Precast Junction Boxes (PJB). It details structural wall thicknesses, slab requirements, and reinforcement schedules across various box sizes and fill heights up to 20 feet. Engineers must use these tables to verify that selected precast units meet structural and hydraulic demands. Connection requirements specify minimum reinforcing steel ratios, knockout configurations, and slab-to-wall connection details. End treatments and pipe connection angles must be verified against hydraulic gradients. Designers should cross-reference CD-PB-20 and CD-PJB-20 for complete fabrication details.",
        "constraints": "Fill height: up to 20 ft | Design tables for structural wall and slab schedules",
        "file_name": "CD-PDD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PDD-20.pdf"
    },
    {
        "code": "CD-PJB-20",
        "category": "Precast Inlets & Manholes",
        "title": "Precast Junction Box",
        "summary": "This standard details precast concrete junction boxes utilized for aligning, splitting, or turning major storm sewer trunk lines. The structural walls and base slabs require minimum thicknesses ranging from 6 inches to 10 inches depending on box span and burial depth. Design engineers must check internal flow velocities, benching details, and localized turbulence forces. Connection details specify interlocking precast joints with mastic sealant and reinforced monolithic corner connections. Pipe penetrations require resilient waterstops or non-shrink grout collars. Engineers should review CD-PRM-23 and CD-PDD-20 for design data support.",
        "constraints": "Wall/Slab thickness: 6\" to 10\" min | Resilient waterstops and mastic joints",
        "file_name": "CD-PJB-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PJB-20.pdf"
    },
    {
        "code": "CD-PBGC-24",
        "category": "Precast Inlets & Manholes",
        "title": "Pipe and Box Grouted Connections",
        "summary": "This standard specifies construction details and material requirements for grouted connections joining pipes and precast boxes. Minimum grout collar thickness around pipe penetrations is specified at 3 inches to ensure proper load transfer and watertightness. Engineers must examine annular space dimensions, surface roughening requirements on precast units, and non-shrink grout specifications. Connection details require mechanical bonding agents and reinforcement dowels where structural continuity is specified. End treatments and pipe joint collars must be inspected for crack prevention. Designers should review CD-PB-20 and CD-PJB-20 when applying these connection details.",
        "constraints": "Grout collar thickness: 3\" min | Non-shrink grout and mechanical bonding",
        "file_name": "CD-PBGC-24.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PBGC-24.pdf"
    },
    {
        "code": "CD-EX-PB-20",
        "category": "Precast Inlets & Manholes",
        "title": "Example of PB Reducing Slab & Reduced Riser Sizes",
        "summary": "This reference sheet provides design examples and configuration charts for reducing slabs and riser transitions in precast bases (PB). It details structural slab thicknesses starting at 8 inches to transition from large base chambers to standard smaller riser necks. Engineers must verify eccentric and concentric opening layouts, reinforcement curtailment, and local bending moments. Connection details require structural keyway joints filled with approved non-shrink grout. End configurations and manhole frame placement must be verified for surface drainage grading. Designers should pair this sheet directly with CD-PB-20 and CD-PDD-20.",
        "constraints": "Reducing slab thickness: 8\" min | Keyway joint grouting requirements",
        "file_name": "CD-EX-PB-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-EX-PB-20.pdf"
    },
    {
        "code": "CD-PB-20",
        "category": "Precast Inlets & Manholes",
        "title": "Precast Base",
        "summary": "This standard details standard precast concrete base units serving as foundational structures for inlets, manholes, and junction boxes. Base slab and vertical wall thicknesses are standardized at a minimum of 6 inches to 8 inches for heavy-duty support. Design engineers must evaluate subgrade bearing capacity, leveling bed thickness, and buoyant uplift forces in high groundwater tables. Connection details mandate resilient precast joint gaskets, knockouts, and grouted benching configurations. Inlet and outlet pipe alignments must match invert elevations precisely. Engineers should review CD-EX-PB-20 and CD-PDD-20 for comprehensive sizing guidance.",
        "constraints": "Base/Wall thickness: 6\" to 8\" min | Subgrade bearing and buoyant uplift checks",
        "file_name": "CD-PB-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PB-20.pdf"
    },
    {
        "code": "CD-BD3-20",
        "category": "Inlets & Drains",
        "title": "Bridge Drain Details (Welded) with Cast Options",
        "summary": "This standard provides engineering drawings for welded bridge drainage scuppers and downspouts that incorporate optional cast metal components. Structural metal wall thicknesses range from 0.5 inches to 1.0 inch for heavy-duty structural steel and cast iron frames. Engineers must evaluate vibrational fatigue, corrosion protection coatings, and hydraulic collection capacity across bridge decks. Connection details specify welded structural steel brackets bolted directly to bridge girders or deck overhangs with stainless steel hardware. Outflow routing connects to suspended drainage piping systems. Designers should cross-reference CD-BD1-20 and CD-BD2-20 for alternative bridge drainage designs.",
        "constraints": "Metal wall thickness: 0.5\" to 1.0\" min | Girder-mounted welded/cast brackets",
        "file_name": "CD-BD3-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-BD3-20.pdf"
    },
    {
        "code": "CD-BD2-20",
        "category": "Inlets & Drains",
        "title": "Bridge Drain Details (Welded)",
        "summary": "This drawing outlines standard all-welded structural steel bridge deck drainage assemblies and scupper grates. Structural steel plate thicknesses are specified at a minimum of 0.5 inches to withstand highway dynamic loading and harsh environmental exposure. Design engineers must check deck drainage collection efficiency, scupper spacing, and clearance around structural steel girders. Connection details require precision field welding or high-strength bolted connections to bridge superstructure elements. Downspout drop pipes must be rigidly braced. Engineers should review CD-BD1-20 and CD-BD3-20 for cast and hybrid options.",
        "constraints": "Steel plate thickness: 0.5\" min | Structural welded fabrication details",
        "file_name": "CD-BD2-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-BD2-20.pdf"
    },
    {
        "code": "CD-BD1-20",
        "category": "Inlets & Drains",
        "title": "Bridge Drain Details (Cast)",
        "summary": "This standard specifies design requirements for cast metal bridge deck drains and catch basins. Cast iron and steel component wall thicknesses are maintained at a minimum of 0.75 inches for structural durability and corrosion resistance. Engineers must review deck slope integration, grate slip-resistance ratings, and clear opening ratios. Connection details involve heavy-duty casting flanges bolted securely into bridge deck formwork blockouts with corrosion-resistant anchors. Outfall pipes connect to under-deck collection manifolds. Designers should cross-reference CD-BD2-20 and CD-BD3-20 for welded configurations.",
        "constraints": "Cast wall thickness: 0.75\" min | Deck formwork casting flanges and anchors",
        "file_name": "CD-BD1-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-BD1-20.pdf"
    },
    {
        "code": "CD-SD-20",
        "category": "Inlets & Drains",
        "title": "Roadway Slotted Drain",
        "summary": "This standard details continuous linear slotted drain systems embedded in roadway pavements for sheet flow interception. Structural channel wall and throat thicknesses comply with heavy-duty steel pipe or polymer concrete standards starting at 0.25 inches. Design engineers must verify longitudinal pavement slopes, sheet flow depths, and clogging potential in heavy sediment areas. Connection details require secure coupling bands, concrete encasement cradles, and cleanout access points. Outlets must tie into standard catch basins or manholes. Engineers should review CD-IL-20 and standard inlet drawings for point-source drainage alternatives.",
        "constraints": "Channel/Wall thickness: 0.25\" min steel | Concrete encasement cradle",
        "file_name": "CD-SD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SD-20.pdf"
    },
    {
        "code": "CD-IL-20",
        "category": "Inlets & Drains",
        "title": "Sloping Inlet Type S with Grate",
        "summary": "This standard outlines structural details for Type S sloping inlets complete with heavy-duty surface grates for ditch and slope drainage. Structural concrete wall and apron thicknesses are specified at a minimum of 6 inches. Engineers must calculate hydraulic capacity on sloping embankments and verify riprap erosion protection around the inlet perimeter. Connection details specify grouted pipe connections and anchor bolts for heavy steel grates. End treatments must blend smoothly with roadside ditch slopes. Designers should cross-reference CD-CCO-23 and CD-SD-20 for other surface drainage solutions.",
        "constraints": "Wall/Apron thickness: 6\" min | Perimeter riprap slope protection details",
        "file_name": "CD-IL-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-IL-20.pdf"
    },
    {
        "code": "CD-CCO-23",
        "category": "Inlets & Drains",
        "title": "Cast-In-Place Curb Inlet Outside Roadway",
        "summary": "This standard provides construction details for cast-in-place (CIP) curb inlets situated outside primary travel lanes. Structural wall and slab thicknesses are designed at a minimum of 8 inches of reinforced concrete to withstand heavy shoulder loads and earth pressures. Engineers must evaluate subgrade stability, reinforcement steel placement, and clear opening dimensions. Connection details require dowelled construction joints tied into adjacent concrete curbs and gutters, along with blockouts for storm pipes. Outlets require standard headwall connections. Designers should review CD-PCO-23 for precast alternatives and CD-IL-20 for sloping inlets.",
        "constraints": "CIP wall/slab thickness: 8\" min | Dowelled curb joints and pipe blockouts",
        "file_name": "CD-CCO-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CCO-23.pdf"
    },
    {
        "code": "CD-SP-20",
        "category": "Stock Pass",
        "title": "Livestock Pass Under Roadway",
        "summary": "This standard details structural sizing and geometry for livestock underpasses beneath highway embankments. Concrete box wall and slab thicknesses range from 8 inches to 12 inches depending on span and deep fill requirements up to 25 feet. Design engineers must verify internal vertical clearance, drainage sloping to prevent ponding, and security fencing interfaces. Connection details incorporate standard box culvert tongue-and-groove joints with mastic seals and wingwall anchorages. End treatments require wingwalls and safety guardrails. Engineers should compare these structural dimensions with CD-XBC box culvert standards.",
        "constraints": "Wall/Slab thickness: 8\" to 12\" min | Fill height up to 25 ft | Drainage slope required",
        "file_name": "CD-SP-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SP-20.pdf"
    },
    {
        "code": "CD-GSES-PD-20",
        "category": "Safety End Treatment",
        "title": "Galvanized Steel End 12\"–60\" Diameter P/D",
        "summary": "This standard specifies parallel drainage galvanized steel safety end treatments for circular pipes ranging from 12 inches to 60 inches in diameter. Sheet metal thickness complies with AASHTO specifications starting at 0.064 inches up to 0.138 inches based on diameter. Engineers must review grading slopes, safety bar spacing, and toe plate embedment depths. Connection details mandate annular band couplers or bolted stub connections to secure the safety end securely to the mainline pipe. End treatments must align with parallel roadside slopes to eliminate fixed hazards. Designers should cross-reference CD-GSES-CD-20 for cross drainage and CD-SETP standards.",
        "constraints": "Metal thickness: 0.064\" to 0.138\" | Pipe diameter: 12\" to 60\" | Parallel slope alignment",
        "file_name": "CD-GSES-PD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-GSES-PD-20.pdf"
    },
    {
        "code": "SETP-PD",
        "category": "Safety End Treatment (Pipe)",
        "title": "Parallel Drainage for 12\"-72\" Diameter",
        "summary": "This standard establishes structural design details for parallel drainage safety end treatments supporting circular pipe culverts ranging from 12 inches to 72 inches in diameter. The precast or cast-in-place concrete apron requires a minimum structural thickness of 6 inches to withstand lateral soil pressures and parallel mowed slope maintenance equipment. Design engineers must evaluate flow velocities, embankment slope transitions, and toe wall embedment depths to prevent undermining under high discharge events. Connection details mandate secure anchor bolts, rigid pipe stub connections, and grouted collar joints to eliminate differential settlement between the pipe barrel and the end treatment. Safety grates and transverse barrier bars must be inspected for proper spacing and breakaway compliance. Engineers should cross-reference CD-SETP-CD-20 for cross drainage applications and review CD-GSES-PD-20 for galvanized steel alternatives.",
        "constraints": "Diameter: 12\" to 72\" | Min slab thickness: 6\" | Parallel slope alignment",
        "file_name": "CD-SETP-PD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-PD-20.pdf"
    },
    {
        "code": "SETP-CD-A",
        "category": "Safety End Treatment (Pipe)",
        "title": "Cross Drainage for Design 1-7 Arch",
        "summary": "This standard details cross drainage safety end treatments specifically engineered for Design 1 through 7 structural arch pipes under highway mainlines. The reinforced concrete headwall and apron assembly features minimum concrete thicknesses of 8 inches to resist high headwater pressures and cross-flow turbulence. Engineers must calculate hydraulic discharge capacities, inlet control losses, and required riprap apron sizing at the downstream transition. Connection details require specialized arch-shaped collar forms, non-shrink grout seals, and continuous dowel reinforcement tying into the mainline pipe sections. Wingwall geometry and flare angles must be verified against embankment cross-slopes. Designers are encouraged to examine CD-SETP-PDA-20 for parallel drainage arch options and CD-CH-FWA standards.",
        "constraints": "Arch Design: 1 to 7 | Min concrete thickness: 8\" | Cross drainage headwall",
        "file_name": "CD-SETP-CDA-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-CDA-20.pdf"
    },
    {
        "code": "SETP-PD-A",
        "category": "Safety End Treatment (Pipe)",
        "title": "Parallel Drainage for Design 1-9 Arch",
        "summary": "This standard specifies parallel drainage safety end treatments for arch pipe installations spanning Design 1 through 9 profiles along highway side slopes. Structural concrete aprons require a minimum thickness of 6 inches to handle earth cover loads and parallel drainage flows. Design engineers must examine clear zone safety requirements, hinge point grading, and hydraulic transition efficiency for non-circular geometries. Connection details incorporate custom arch connector collars, rubber gasket seals, and mechanical tie-downs to prevent joint separation. End treatments must merge smoothly with parallel ditch lines to eliminate vehicle snagging hazards. Engineers should cross-reference CD-SETP-CD-A for cross drainage and CD-CH-PW-A standards for parallel wing configurations.",
        "constraints": "Arch Design: 1 to 9 | Min slab thickness: 6\" | Parallel drainage grading",
        "file_name": "CD-SETP-PDA-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-PDA-20.pdf"
    },
    {
        "code": "SETP-FW-0",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 0 Degree Skew C/D Round",
        "summary": "This standard outlines cross drainage safety end treatments featuring flared wingwalls at a 0-degree skew for round pipe culverts. Structural wall and footing thicknesses are standardized at a minimum of 8 inches of reinforced concrete for durability against hydraulic forces. Engineers must verify headwater elevation limits, approach channel velocities, and downstream energy dissipation requirements. Connection details require positive mechanical anchoring, grouted collar joints, and keyway construction joints between the pipe and the wingwall structure. Wing flare angles must align with natural channel bank geometry. Designers should review CD-SETP-FW-15 and CD-SETP-FW-30 for skewed applications and CD-CH-FW-0 for non-safety end headwalls.",
        "constraints": "Skew: 0° | Min wall thickness: 8\" | Cross drainage flared wings",
        "file_name": "CD-SETP-FW0-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FW0-20.pdf"
    },
    {
        "code": "SETP-FW-15",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 15 Degree Skew C/D Round",
        "summary": "This standard provides engineering details for cross drainage safety end treatments with flared wingwalls set at a 15-degree skew for round pipes. Minimum concrete thickness for walls and aprons is 8 inches to resist asymmetrical earth pressures and stream flow turbulence. Design engineers must evaluate alignment angles, flow contraction losses, and skew-induced structural bending moments. Connection details mandate reinforced concrete collars, dowelled footings, and resilient joint materials between the pipe barrel and headwall. Riprap protection must be detailed along the skewed bank interface to prevent localized scour. Engineers should cross-reference CD-SETP-FW-0 and CD-SETP-FW-30 for alternative skew angles.",
        "constraints": "Skew: 15° | Min wall thickness: 8\" | Skewed flared wing alignment",
        "file_name": "CD-SETP-FW15-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FW15-20.pdf"
    },
    {
        "code": "SETP-FW-30",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 30 Degree Skew C/D Round",
        "summary": "This standard details cross drainage safety end treatments incorporating 30-degree skewed flared wingwalls for circular pipe culverts. Structural elements require a minimum thickness of 8 inches of reinforced concrete to safely accommodate acute angle stress distributions. Engineers must review stream alignment angles, wingwall length requirements, and differential earth loading across the skewed structure. Connection details require robust dowel reinforcement, non-shrink grout packings, and positive pipe-to-headwall mechanical ties. Protection aprons must extend across the entire skewed transition. Designers should review CD-SETP-FW-15 and CD-CH-FW-30 standards for comparable geometry.",
        "constraints": "Skew: 30° | Min concrete thickness: 8\" | Acute angle stress distribution",
        "file_name": "CD-SETP-FW30-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FW30-20.pdf"
    },
    {
        "code": "SETP-FW-A-0",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 0 Skew C/D Arch",
        "summary": "This standard specifies cross drainage safety end treatments with 0-degree skewed flared wings specifically designed for arch pipe culverts. Minimum concrete wall and footing thickness is 8 inches to accommodate arch thrust loads and hydraulic forces. Design engineers must check critical rise-to-span ratios, arch perimeter soil pressure distribution, and inlet capacity. Connection details require custom arch-profile formwork, grouted keyway joints, and mechanical anchors connecting the pipe crown to the headwall. Scour protection aprons are required at the invert. Engineers should cross-reference CD-SETP-FWA-15, CD-SETP-FWA-30, and CD-CH-FW-A-0 standards.",
        "constraints": "Arch Pipe | Skew: 0° | Min wall thickness: 8\" | Thrust load distribution",
        "file_name": "CD-SETP-FWA0-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FWA0-20.pdf"
    },
    {
        "code": "SETP-FW-A-15",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 15 Skew C/D Arch",
        "summary": "This standard provides details for cross drainage safety end treatments featuring 15-degree skewed flared wings for arch pipe installations. Structural concrete thickness is maintained at a minimum of 8 inches to handle asymmetric hydraulic and soil loads. Engineers must evaluate skew geometry effects on arch thrust lines, wingwall cantilever moments, and transition grading. Connection details mandate reinforced dowel connections, non-shrink grout seals, and specialized arch connection collars. Toe protection and riprap placement must be verified against skewed flow separation. Designers should review CD-SETP-FWA-0 and CD-SETP-FWA-30 for other skew options.",
        "constraints": "Arch Pipe | Skew: 15° | Min thickness: 8\" | Skew-induced moment checks",
        "file_name": "CD-SETP-FWA15-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FWA15-20.pdf"
    },
    {
        "code": "SETP-FW-A-30",
        "category": "Safety End Treatment (Pipe)",
        "title": "Flared Wings 30 Skew C/D Arch",
        "summary": "This standard outlines cross drainage safety end treatments with 30-degree skewed flared wingwalls for arch pipe culverts. Minimum concrete thickness is 8 inches to withstand severe acute angle geometric stresses and high-velocity flows. Design engineers must examine stream alignment, differential earth pressures, and wingwall structural stability. Connection details require positive mechanical ties, continuous footing dowels, and grouted arch collars. Scour aprons must be extended along the acute angle side. Engineers should cross-reference CD-SETP-FWA-15 and CD-CH-FW-A-30 standards for related designs.",
        "constraints": "Arch Pipe | Skew: 30° | Min thickness: 8\" | Acute angle structural stability",
        "file_name": "CD-SETP-FWA30-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SETP-FWA30-20.pdf"
    },
    {
        "code": "PSET-SC",
        "category": "Safety End Treatment (Pipe)",
        "title": "Precast End Treatment C/D Sq",
        "summary": "This standard details precast square cross drainage end treatments for pipe culverts, offering rapid field installation alternatives to cast-in-place headwalls. Structural precast walls and base slabs require a minimum thickness of 6 inches to 8 inches for handling, lifting, and in-service loading. Engineers must verify lifting insert capacities, subgrade leveling bed compaction, and hydraulic flow alignment. Connection details specify interlocking precast joints sealed with mastic or rubber gaskets, along with grouted pipe collars. End treatments must coordinate with safety barrier grates. Designers should review PSET-SP for parallel drainage and CD-PSET-RC for round precast options.",
        "constraints": "Precast square | Min wall/slab thickness: 6\" to 8\" | Cross drainage",
        "file_name": "CD-PSET-SC-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSET-SC-21.pdf"
    },
    {
        "code": "PSET-SP",
        "category": "Safety End Treatment (Pipe)",
        "title": "Precast End Treatment P/D Sq",
        "summary": "This standard specifies precast square parallel drainage end treatments designed for pipe culverts situated along highway side slopes. Precast structural components feature minimum thicknesses of 6 inches to withstand earth cover and maintenance vehicle loads. Design engineers must check clear zone grading, side slope transition profiles, and drainage interception efficiency. Connection details mandate resilient joint gaskets, mechanical tie bars, and non-shrink grouted pipe penetrations. Outlet aprons must be stabilized against erosion. Engineers should cross-reference CD-PSET-SC for cross drainage and CD-PSET-RP for round precast parallel units.",
        "constraints": "Precast square | Min thickness: 6\" | Parallel roadside drainage",
        "file_name": "CD-PSET-SP-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSET-SP-21.pdf"
    },
    {
        "code": "PSET-RC",
        "category": "Safety End Treatment (Pipe)",
        "title": "Precast End Treatment C/D Round",
        "summary": "This standard outlines precast round cross drainage end treatments for circular pipe culverts across highway alignments. Structural wall and apron thicknesses are standardized at a minimum of 6 inches to 8 inches. Engineers must evaluate hydraulic capacity, approach flow conditions, and buoyant stability in prone drainage areas. Connection details require tongue-and-groove precast joints with rubber gaskets, secure anchoring hardware, and grouted annular spaces around incoming pipes. Slope paving and riprap details must be integrated. Designers should review CD-PSET-RP for parallel drainage and CD-PSET-RR for riprap stabilization.",
        "constraints": "Precast round | Min thickness: 6\" to 8\" | Cross drainage application",
        "file_name": "CD-PSET-RC-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSET-RC-20.pdf"
    },
    {
        "code": "PSET-RP",
        "category": "Safety End Treatment (Pipe)",
        "title": "Precast End Treatment P/D Round",
        "summary": "This standard details precast round parallel drainage end treatments for circular pipes located in roadside clear zones. Precast structural sections maintain a minimum concrete thickness of 6 inches. Design engineers must verify side slope grading compatibility, safety bar positioning, and hydraulic discharge rates. Connection details incorporate flexible joint boots, rubber gaskets, and positive mechanical locking devices to prevent separation during backfilling. Downstream channel protection is mandatory. Engineers should cross-reference CD-PSET-RC for cross drainage and CD-PSET-RR for riprap apron requirements.",
        "constraints": "Precast round | Min thickness: 6\" | Parallel roadside alignment",
        "file_name": "CD-PSET-RP-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSET-RP-20.pdf"
    },
    {
        "code": "PSET-RR",
        "category": "Safety End Treatment (Pipe)",
        "title": "Precast End Treatment Riprap Details",
        "summary": "This standard provides comprehensive riprap apron and slope stabilization details specifically tailored for precast end treatments. Concrete riprap or stone thickness is specified at a minimum of 6 inches placed over approved filter fabric. Engineers must calculate peak outlet velocities, shear stress limits, and apron sizing to prevent downstream channel erosion. Connection details require positive toe wall embedment into stable channel subgrades and grouted joints around precast end aprons. Transition grading must ensure smooth flow exits without turbulence. Designers should review all CD-PSET series drawings and CD-Riprap standards for complete erosion control coordination.",
        "constraints": "Riprap thickness: 6\" min | Filter fabric underlayment | Toe wall embedment",
        "file_name": "CD-PSET-RR-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-PSET-RR-20.pdf"
    },
    {
        "code": "GS-ES-CD",
        "category": "Safety End Treatment (Pipe)",
        "title": "Galvanized Steel End 12\"-60\" Diameter C/D",
        "summary": "This standard specifies cross drainage galvanized steel safety end treatments for circular pipes ranging from 12 inches to 60 inches in diameter. Metal sheet thicknesses comply with AASHTO specifications starting at 0.064 inches up to 0.138 inches based on pipe diameter. Design engineers must evaluate cross-flow hydraulic capacity, safety bar spacing, and toe plate embedment depths. Connection details require annular band couplers, bolt-on stub connections, and concrete anchor collars to secure the steel structure against uplift forces. End treatments must align with roadway side slopes. Engineers should review CD-GSES-PD-20 for parallel drainage and CD-SETP standards.",
        "constraints": "Diameter: 12\" to 60\" | Metal thickness: 0.064\" to 0.138\" | Cross drainage",
        "file_name": "CD-GSES-CD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-GSES-CD-20.pdf"
    },
    {
        "code": "GS-ES-PD",
        "category": "Safety End Treatment (Pipe)",
        "title": "Galvanized Steel End 12\"-60\" Diameter P/D",
        "summary": "This standard outlines parallel drainage galvanized steel safety end treatments for circular pipes from 12 inches to 60 inches in diameter. Corrugated steel sheet thicknesses range from 0.064 inches to 0.138 inches to provide structural rigidity under soil backfill. Engineers must verify parallel slope grading, safety bar configurations, and erosion protection at the toe plate. Connection details dictate corrugated band couplers, connecting hardware, and positive fastening systems to maintain watertight and soil-tight joints. Outlets must discharge safely into roadside ditches. Designers should cross-reference CD-GSES-CD-20 and CD-SETP-PD-20 standards.",
        "constraints": "Diameter: 12\" to 60\" | Metal thickness: 0.064\" to 0.138\" | Parallel drainage",
        "file_name": "CD-GSES-PD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-GSES-PD-20.pdf"
    },
    {
        "code": "MC-MD",
        "category": "Multi-Box Culverts",
        "title": "Cast-In-Place Miscellaneous Details",
        "summary": "This standard provides miscellaneous structural details for cast-in-place multi-box concrete culverts, including construction joints, waterstops, and fillet dimensions. Minimum structural wall and slab thicknesses comply with standard box design tables, typically starting at 8 inches. Design engineers must evaluate thermal movement joints, shrinkage reinforcement ratios, and waterproofing details between barrel sections. Connection details require hydrophilic waterstops, continuous dowel reinforcement, and keyway construction joints. End treatments must interface with standard wingwalls and aprons. Engineers should review CD-SCC-MD-20 for single box equivalents and CD-BCS-20 for supplemental wings.",
        "constraints": "Min wall/slab thickness: 8\" | Hydrophilic waterstops | Shrinkage reinforcement",
        "file_name": "CD-MC-MD-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC-MD-20.pdf"
    },
    {
        "code": "MC-3-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 3' Spans for Lengthening",
        "summary": "This standard details cast-in-place multi-box 3-foot span configurations specifically engineered for structural culvert lengthening projects. Minimum top and bottom slab thicknesses are engineered at 8 inches to match existing barrel sections across fill heights up to 23 feet. Engineers must examine existing rebar dowel extensions, concrete surface preparation, and differential settlement potential between old and new barrel segments. Connection details require mechanical splice couplers or drilled-and-epoxied dowels with rigorous embedment depths. End treatments must align with existing wingwalls or new extension headwalls. Designers should cross-reference CD-MC-4-23 and CD-XBC standards.",
        "constraints": "Span: 3 ft | Min thickness: 8\" | Fill height: up to 23 ft | Lengthening dowels",
        "file_name": "CD-MC323-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC323-20.pdf"
    },
    {
        "code": "MC-4-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 4' Spans for Lengthening",
        "summary": "This standard outlines cast-in-place multi-box 4-foot span details designed for structural extension and lengthening operations under deep fills. Structural slab and wall thicknesses are maintained at a minimum of 8 inches. Design engineers must review existing structure records, dowel pullout strengths, and moment transfer across the construction joint. Connection details mandate epoxied reinforcing dowels, shear keys, and matching interior flowline elevations. Wingwall extensions must tie into the new barrels seamlessly. Engineers should review CD-MC-3-23 and standard multi-box culvert drawings for complete extension coordination.",
        "constraints": "Span: 4 ft | Min thickness: 8\" | Fill height: up to 23 ft | Extension joints",
        "file_name": "CD-MC423-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC423-20.pdf"
    },
    {
        "code": "MC-5-20",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 5' Spans thru 20'",
        "summary": "This standard provides structural design configurations for cast-in-place multi-box 5-foot span culverts subjected to fill heights up to 20 feet. Wall and slab thicknesses range from 8 inches to 10 inches of reinforced concrete based on earth load schedules. Engineers must calculate bending moments, shear forces, and live load distribution across multi-barrel configurations. Connection details require monolithic wall-to-slab haunches, continuous transverse reinforcement, and waterstopped vertical construction joints. End treatments must coordinate with standard wingwall standards. Designers should cross-reference CD-MC-5-23 for deeper fills and CD-BCS-20 for supplemental wings.",
        "constraints": "Span: 5 ft | Fill: Thru 20 ft | Min thickness: 8\" to 10\" | Haunch detailing",
        "file_name": "CD-MC520-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC520-20.pdf"
    },
    {
        "code": "MC-5-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 5' Spans thru 23' Fill",
        "summary": "This standard details cast-in-place multi-box 5-foot span culverts engineered for deep embankment fills up to 23 feet. Structural concrete thicknesses for top slabs, bottom slabs, and exterior walls are increased to a minimum of 10 inches to withstand high earth pressures. Design engineers must evaluate heavy dead loads, soil-structure interaction, and crack control reinforcement spacing. Connection details specify robust shear keys, heavy dowel reinforcement, and waterproof joint seals. Wingwalls must be designed for maximum soil thrust. Engineers should review CD-MC-5-20 and CD-MC-6-23 standards for comparative sizing.",
        "constraints": "Span: 5 ft | Fill: Thru 23 ft | Min thickness: 10\" | Deep fill reinforcement",
        "file_name": "CD-MC523-23.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC523-23.pdf"
    },
    {
        "code": "MC-6-16",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 6' Spans thru 16' Fill",
        "summary": "This standard outlines cast-in-place multi-box 6-foot span culvert designs for standard fills up to 16 feet. Minimum structural thickness for slabs and walls is specified at 8.5 inches of reinforced concrete. Engineers must verify hydraulic flow capacity across multiple barrels, sediment deposition risks, and HL-93 live load distribution. Connection details mandate continuous internal haunches, keyed construction joints, and waterstops between adjacent barrel pours. End treatments require standard wingwalls and aprons. Designers should cross-reference CD-MC-6-20 and CD-MC-6-23 for deeper fill options.",
        "constraints": "Span: 6 ft | Fill: Thru 16 ft | Min thickness: 8.5\" | Multi-barrel flow checks",
        "file_name": "CD-MC616-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC616-20.pdf"
    },
    {
        "code": "MC-6-20",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 6' Spans thru 20' Fill",
        "summary": "This standard provides structural details for cast-in-place multi-box 6-foot span culverts accommodating fills up to 20 feet. Concrete slab and wall thicknesses are standardized at a minimum of 9 inches to handle increased earth dead loads. Design engineers must check principal bending stresses, shear reinforcement requirements in exterior walls, and foundation bearing pressures. Connection details incorporate robust dowelled joints, hydrophilic waterstops, and monolithic haunch placements. Wingwall connection details must be verified against lateral earth pressures. Engineers should review CD-MC-6-16 and CD-MC-7-20 standards.",
        "constraints": "Span: 6 ft | Fill: Thru 20 ft | Min thickness: 9\" | Foundation bearing checks",
        "file_name": "CD-MC620-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC620-20.pdf"
    },
    {
        "code": "MC-6-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 6' Spans thru 23' Fill",
        "summary": "This standard details cast-in-place multi-box 6-foot span culverts engineered for maximum deep fill conditions up to 23 feet. Minimum structural concrete thickness is 10 inches across top slabs, bottom slabs, and vertical walls. Engineers must evaluate severe earth loads, temperature gradient stresses, and crack control parameters. Connection details specify heavy reinforcing steel schedules, shear friction dowels, and positive waterstop placement. End treatments require heavily reinforced wingwalls and cut-off walls. Designers should cross-reference CD-MC-6-20 and CD-MC-8-23 standards.",
        "constraints": "Span: 6 ft | Fill: Thru 23 ft | Min thickness: 10\" | Temperature and crack control",
        "file_name": "CD-MC623-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC623-20.pdf"
    },
    {
        "code": "MC-7-10",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 7' Spans thru 10' Fill",
        "summary": "This standard outlines cast-in-place multi-box 7-foot span culvert configurations for shallow to moderate fills up to 10 feet. Structural slab and wall thicknesses are established at a minimum of 9 inches of reinforced concrete. Design engineers must examine live load impact factors, wheel load distribution through shallow pavement sections, and hydraulic efficiency. Connection details require standard haunch dimensions, keyed construction joints, and joint sealants. Wingwall and apron transitions must be detailed to prevent scour. Engineers should review CD-MC-7-16 and CD-MC-7-20 for deeper fill requirements.",
        "constraints": "Span: 7 ft | Fill: Thru 10 ft | Min thickness: 9\" | Shallow fill live load checks",
        "file_name": "CD-MC710-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC710-20.pdf"
    },
    {
        "code": "MC-7-16",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 7' Spans thru 16' Fill",
        "summary": "This standard provides structural drawings for cast-in-place multi-box 7-foot span culverts under fills up to 16 feet. Minimum structural concrete thickness is 9.5 inches for walls and slabs. Engineers must evaluate dead load earth pressures, moment distributions, and multi-barrel interaction forces. Connection details mandate continuous reinforcing steel across interior walls, shear keys, and waterstopped vertical joints. End treatments must align with standard wingwall configurations. Designers should cross-reference CD-MC-7-10 and CD-MC-7-20 standards.",
        "constraints": "Span: 7 ft | Fill: Thru 16 ft | Min thickness: 9.5\" | Multi-barrel interaction",
        "file_name": "CD-MC716-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC716-20.pdf"
    },
    {
        "code": "MC-7-20",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 7' Spans thru 20' Fill",
        "summary": "This standard details cast-in-place multi-box 7-foot span culverts designed for substantial earth fills up to 20 feet. Structural concrete thickness is specified at a minimum of 10 inches to resist high vertical soil loads. Design engineers must check shear capacity in exterior walls, foundation bearing pressures, and settlement potential. Connection details require heavy dowel reinforcement, keyed joints, and hydrophilic waterstops. Wingwalls require heavy cantilever design. Engineers should review CD-MC-7-16 and CD-MC-7-23 standards for adjacent fill limits.",
        "constraints": "Span: 7 ft | Fill: Thru 20 ft | Min thickness: 10\" | Shear capacity checks",
        "file_name": "CD-MC720-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC720-20.pdf"
    },
    {
        "code": "MC-7-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 7' Spans thru 23' Fill",
        "summary": "This standard outlines cast-in-place multi-box 7-foot span culverts engineered for deep fills up to 23 feet. Minimum structural thickness is 11 inches across all slabs and walls to handle intense static and dynamic earth loads. Engineers must evaluate maximum bending moments, temperature reinforcement, and crack control standards. Connection details specify heavy-duty shear keys, epoxy-coated dowels, and positive waterstop integration. End treatments require robust headwalls and wingwalls. Designers should cross-reference CD-MC-7-20 and CD-MC-8-23 standards.",
        "constraints": "Span: 7 ft | Fill: Thru 23 ft | Min thickness: 11\" | Heavy earth load design",
        "file_name": "CD-MC723-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC723-20.pdf"
    },
    
    {
        "code": "MC-8-16",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 8' Spans thru 16' Fill",
        "summary": "This standard details structural design configurations for cast-in-place multi-box 8-foot span culverts under fill heights up to 16 feet. Minimum structural thickness for top slabs, bottom slabs, and exterior walls is established at 9.5 inches of reinforced concrete. Design engineers must calculate primary bending moments, shear distribution across multiple barrels, and wheel load impact attenuation through shallow pavement covers. Connection details specify continuous internal haunches, keyed construction joints, and waterstopped vertical pour interfaces. End treatments require robust wingwalls and cut-off aprons. Engineers should cross-reference CD-MC-8-20 and CD-MC-8-23 standards for deep fill variations.",
        "constraints": "Span: 8 ft | Fill: Thru 16 ft | Min thickness: 9.5\" | Multi-barrel shear checks",
        "file_name": "CD-MC816-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC816-20.pdf"
    },
    {
        "code": "MC-8-20",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 8' Spans thru 20' Fill",
        "summary": "This standard provides engineering drawings for cast-in-place multi-box 8-foot span culverts subjected to earth fills up to 20 feet. Structural concrete thickness is increased to a minimum of 10.5 inches to safely withstand high vertical and lateral soil pressures. Engineers must evaluate foundation bearing pressures, differential settlement risks, and crack control reinforcement spacing. Connection details require heavy dowel reinforcement, epoxy-coated tie bars, and hydrophilic waterstops in all vertical construction joints. Wingwalls must be checked for maximum cantilever soil thrust. Designers should review CD-MC-8-16 and CD-MC-8-23 for adjacent fill limits.",
        "constraints": "Span: 8 ft | Fill: Thru 20 ft | Min thickness: 10.5\" | Foundation bearing checks",
        "file_name": "CD-MC820-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC820-20.pdf"
    },
    {
        "code": "MC-8-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 8' Spans thru 23' Fill",
        "summary": "This standard outlines cast-in-place multi-box 8-foot span culverts engineered for maximum deep fill conditions up to 23 feet. Minimum structural thickness is specified at 12 inches across all top slabs, bottom slabs, and vertical walls to handle severe earth loads. Design engineers must evaluate thermal gradient stresses, heavy static dead loads, and precise crack control parameters. Connection details specify heavy-duty shear keys, shear friction dowels, and positive waterstop integration. End treatments require heavily reinforced headwalls. Engineers should cross-reference CD-MC-8-20 and CD-MC-10-23 standards.",
        "constraints": "Span: 8 ft | Fill: Thru 23 ft | Min thickness: 12\" | Deep fill load distribution",
        "file_name": "CD-MC823-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC823-20.pdf"
    },
    {
        "code": "MC-10-10",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 10' Spans thru 10' Fill",
        "summary": "This standard provides structural details for cast-in-place multi-box 10-foot span culverts designed for shallow to moderate fills up to 10 feet. Minimum structural slab and wall thickness is set at 10 inches of reinforced concrete. Engineers must examine live load impact factors, large span deflection limits, and hydraulic flow characteristics across wide multi-barrel openings. Connection details mandate standard haunch geometries, keyed construction joints, and flexible joint sealants. Wingwall and apron transitions must be detailed to prevent scour during peak floods. Designers should review CD-MC-10-16 and CD-XBC-10 standards for single-box equivalents.",
        "constraints": "Span: 10 ft | Fill: Thru 10 ft | Min thickness: 10\" | Large span deflection limits",
        "file_name": "CD-MC1010-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC1010-20.pdf"
    },
    {
        "code": "MC-10-16",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 10' Spans thru 16' Fill",
        "summary": "This standard outlines cast-in-place multi-box 10-foot span culvert configurations for intermediate fills up to 16 feet. Structural slab and wall thicknesses are established at a minimum of 11 inches. Design engineers must verify principal bending moments, shear reinforcement in exterior and interior walls, and multi-barrel interaction forces. Connection details require continuous reinforcing steel across interior walls, shear keys, and waterstopped vertical joints. End treatments require standard wingwall configurations. Engineers should cross-reference CD-MC-10-10 and CD-MC-10-20 standards.",
        "constraints": "Span: 10 ft | Fill: Thru 16 ft | Min thickness: 11\" | Interior wall shear reinforcement",
        "file_name": "CD-MC1016-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC1016-20.pdf"
    },
    {
        "code": "MC-10-20",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 10' Spans thru 20' Fill",
        "summary": "This standard details cast-in-place multi-box 10-foot span culverts engineered for substantial earth loads under fills up to 20 feet. Minimum structural concrete thickness is specified at 12 inches. Engineers must evaluate heavy dead loads, soil-structure interaction, and foundation settlement tolerances across wide spans. Connection details specify robust shear keys, heavy dowel reinforcement schedules, and positive waterstop placement. Wingwalls require heavy cantilever design to resist earth pressures. Designers should review CD-MC-10-16 and CD-MC-10-23 standards.",
        "constraints": "Span: 10 ft | Fill: Thru 20 ft | Min thickness: 12\" | Settlement and soil-structure checks",
        "file_name": "CD-MC1020-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC1020-20.pdf"
    },
    {
        "code": "MC-10-23",
        "category": "Multi-Box Culverts",
        "title": "C-I-P 10' Spans thru 23' Fill",
        "summary": "This standard provides comprehensive structural details for cast-in-place multi-box 10-foot span culverts operating under maximum deep fill conditions up to 23 feet. Structural slab and wall thicknesses are designed at a minimum of 13 inches of reinforced concrete. Design engineers must check extreme bending moments, temperature reinforcement ratios, and crack control criteria under high overburden pressures. Connection details mandate heavy-duty shear friction dowels, epoxy-coated reinforcing bars, and waterstops. End treatments require robust headwalls and wingwalls. Engineers should cross-reference all CD-MC series drawings.",
        "constraints": "Span: 10 ft | Fill: Thru 23 ft | Min thickness: 13\" | Maximum overburden pressure design",
        "file_name": "CD-MC1023-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-MC1023-20.pdf"
    },
    {
        "code": "SCC-3 & 4",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 3 ft & 4ft Span Details",
        "summary": "This standard specifies structural design and reinforcement details for single-barrel cast-in-place 3-foot/4-foot span box culverts across variable fill heights. Minimum slab and wall thickness is standardized at 8 inches. Engineers must verify hydraulic capacity, flowline alignment, and concrete cover requirements. Connection details require standard haunch dimensions, construction joint waterstops, and dowel ties into wingwalls. End treatments must coordinate with standard headwall drawings. Designers should cross-reference CD-MC-3-23 for multi-box equivalents and CD-XBC-4-20 for larger single spans.",
        "constraints": "Span: 4 ft | Min wall/slab thickness: 8\" | Single-barrel CIP design",
        "file_name": "CD-SCC34-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC34-21.pdf"
    },
    {
        "code": "SCC-5 & 6",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 5 ft & 6 ft Span Details",
        "summary": "This standard outlines structural drawings for single-barrel cast-in-place 5-foot/6 foot span box culverts under highway embankments. Minimum structural concrete thickness is maintained at 8 inches for walls and slabs. Design engineers must check live load distribution, shear stresses, and subgrade preparation requirements. Connection details mandate keyed construction joints, hydrophilic waterstops, and reinforced haunches. Wingwalls and aprons must be detailed to prevent local scour. Engineers should review CD-XBC-3-20 and CD-XBC-5-20 standards for comparative sizing.",
        "constraints": "Span: 6 ft | Min thickness: 8\" | Subgrade preparation and haunch detailing",
        "file_name": "CD-SCC56-2.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC56-2.pdf"
    },
    {
        "code": "SCC-7-21",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 7 ft Span Details",
        "summary": "This standard provides engineering details for single-barrel cast-in-place 7-foot span box culverts supporting roadway embankments. Structural concrete thickness is maintained at a minimum of 9 inches. Engineers must evaluate dead load earth pressures, moment distributions, and foundation bearing capacities. Connection details mandate robust dowelled joints, shear keys, and hydrophilic waterstops. End treatments require heavily reinforced wingwalls. Designers should cross-reference CD-XBC-6-20 and CD-XBC-8-20 standards.",
        "constraints": "Span: 7 ft | Fill: Up to 20 ft | Min thickness: 8\" to 9\" | Moment and earth pressure checks",
        "file_name": "CD-SCC07-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC07-21.pdf"
    },
    {
        "code": "SCC-8-21",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 8 ft Span Details",
        "summary": "This standard details structural sizing and reinforcement schedules for single-barrel cast-in-place 8-foot span box culverts. Minimum slab and wall thickness is specified at 9.5 inches of reinforced concrete. Design engineers must check span deflections, crack control criteria, and heavy earth load distributions. Connection details specify continuous haunches, keyed joints, and waterstop integration. Wingwall connections must be engineered for lateral soil thrust. Engineers should review CD-XBC-7-20 and CD-XBC-10-20 standards.",
        "constraints": "Span: 8 ft | Min thickness: 8.5\" | HL-93 live load and shallow cover checks",
        "file_name": "CD-SCC08-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC08-21.pdf"
    },
    {
        "code": "SCC-9-21",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 9 ft Span Details",
        "summary": "This standard details structural sizing and reinforcement schedules for single-barrel cast-in-place 9-foot span box culverts. Minimum slab and wall thickness is specified at 9.5 inches of reinforced concrete. Design engineers must check span deflections, crack control criteria, and heavy earth load distributions. Connection details specify continuous haunches, keyed joints, and waterstop integration. Wingwall connections must be engineered for lateral soil thrust. Engineers should review CD-XBC-7-20 and CD-XBC-10-20 standards.",
        "constraints": "Span: 9 ft | Min thickness: 8.5\" | HL-93 live load and shallow cover checks",
        "file_name": "CD-SCC09-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC09-21.pdf"
    },
    {
        "code": "SCC-10-21",
        "category": "Cast-In-Place Box Culverts",
        "title": "Cast-In-Place Box Culvert 10 ft Span Details",
        "summary": "This standard outlines structural design requirements for large single-barrel cast-in-place 10-foot span box culverts. Minimum structural thickness for top slabs, bottom slabs, and walls is established at 10 inches. Engineers must evaluate large span bending moments, shear reinforcement, and settlement tolerances. Connection details require heavy dowel reinforcement, shear keys, and waterstops. End treatments require robust headwalls and wingwalls. Designers should cross-reference CD-XBC-8-20 and CD-MC-10 series multi-box standards.",
        "constraints": "Span: 10 ft | Min thickness: 10\" | Large span bending and shear reinforcement",
        "file_name": "CD-SCC10-21.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-SCC10-21.pdf"
    },
    {
        "code": "CH-FW-0",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 0 Skew Round",
        "summary": "This standard details traditional cast-in-place concrete headwalls featuring flared wingwalls set at a 0-degree skew for circular pipe culverts. Minimum structural wall and footing thickness is 8 inches. Design engineers must calculate headwater elevation limits, approach flow conditions, and riprap apron sizing to prevent scour. Connection details require positive mechanical anchoring, grouted collar joints, and keyway construction joints between the pipe and headwall. Wing flare angles must align with natural channel geometry. Engineers should cross-reference CD-CH-FW-15 and CD-SETP-FW-0 safety end standards.",
        "constraints": "Skew: 0° | Min wall thickness: 8\" | Traditional CIP headwall with flared wings",
        "file_name": "CD-CH-FW0-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FW0-20.pdf"
    },
    {
        "code": "CH-FW-15",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 15 Skew Round",
        "summary": "This standard provides engineering drawings for cast-in-place headwalls with flared wings set at a 15-degree skew for circular pipes. Minimum concrete thickness for walls and aprons is 8 inches to resist asymmetrical earth and water pressures. Engineers must evaluate skewed flow contraction losses, wingwall moment distributions, and toe embedment depth. Connection details mandate reinforced concrete collars, dowelled footings, and resilient joint materials. Riprap protection must be detailed along the skewed bank interface. Designers should review CD-CH-FW-0 and CD-CH-FW-30 standards.",
        "constraints": "Skew: 15° | Min thickness: 8\" | Skewed CIP headwall alignment",
        "file_name": "CD-CH-FW15-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FW15-20.pdf"
    },
    {
        "code": "CH-FW-30",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 30 Skew Round",
        "summary": "This standard outlines cast-in-place headwalls incorporating 30-degree skewed flared wingwalls for circular pipe culverts. Structural elements require a minimum thickness of 8 inches of reinforced concrete to withstand acute angle geometric stresses. Design engineers must review stream alignment, differential earth pressures, and wingwall stability. Connection details require positive mechanical ties, continuous footing dowels, and grouted pipe collars. Scour aprons must extend across the acute angle transition. Engineers should cross-reference CD-CH-FW-15 and CD-SETP-FW-30 standards.",
        "constraints": "Skew: 30° | Min concrete thickness: 8\" | Acute angle structural detailing",
        "file_name": "CD-CH-FW30-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FW30-20.pdf"
    },
    {
        "code": "CH-FWA-0",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 0 Skew Arch",
        "summary": "This standard details cast-in-place headwalls featuring 0-degree skewed flared wings specifically designed for arch pipe culverts. Minimum concrete wall and footing thickness is 8 inches to handle arch thrust loads and hydraulic forces. Engineers must check critical rise-to-span ratios, arch perimeter soil pressure distribution, and inlet capacity. Connection details require custom arch-profile formwork, grouted keyway joints, and mechanical anchors connecting the pipe crown to the headwall. Scour aprons are required at the invert. Designers should review CD-CH-FWA-15 and CD-SETP-FWA-0 standards.",
        "constraints": "Arch Pipe | Skew: 0° | Min thickness: 8\" | Arch thrust load distribution",
        "file_name": "CD-CH-FWA0-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FWA0-20.pdf"
    },
    {
        "code": "CH-FWA-15",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 15 Skew Arch",
        "summary": "This standard provides details for cast-in-place headwalls featuring 15-degree skewed flared wings for arch pipe installations. Structural concrete thickness is maintained at a minimum of 8 inches to handle asymmetric hydraulic and soil loads. Design engineers must evaluate skew geometry effects on arch thrust lines, wingwall cantilever moments, and transition grading. Connection details mandate reinforced dowel connections, non-shrink grout seals, and specialized arch connection collars. Toe protection and riprap placement must be verified against skewed flow separation. Engineers should cross-reference CD-CH-FWA-0 and CD-CH-FWA-30 standards.",
        "constraints": "Arch Pipe | Skew: 15° | Min thickness: 8\" | Skew-induced moment checks",
        "file_name": "CD-CH-FWA15-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FWA15-20.pdf"
    },
    {
        "code": "CH-FWA-30",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Flared Wings 30 Skew Arch",
        "summary": "This standard outlines cast-in-place headwalls with 30-degree skewed flared wingwalls for arch pipe culverts. Minimum concrete thickness is 8 inches to withstand severe acute angle geometric stresses and high-velocity flows. Engineers must examine stream alignment, differential earth pressures, and wingwall structural stability. Connection details require positive mechanical ties, continuous footing dowels, and grouted arch collars. Scour aprons must be extended along the acute angle side. Designers should review CD-CH-FWA-15 and CD-SETP-FWA-30 standards.",
        "constraints": "Arch Pipe | Skew: 30° | Min thickness: 8\" | Acute angle structural stability",
        "file_name": "CD-CH-FWA30-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-FWA30-20.pdf"
    },
    {
        "code": "CH-SW-0",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Straight Wings 0 Skew",
        "summary": "This standard details cast-in-place headwalls with straight wingwalls aligned at a 0-degree skew for pipe culverts. Minimum structural concrete thickness is 8 inches for walls and base slabs. Design engineers must evaluate headwater depths, channel constriction impacts, and downstream energy dissipation requirements. Connection details require dowelled footings, keyway joints, and secure pipe collar connections. Wingwalls must be designed as cantilever retaining walls for backfill soil pressures. Engineers should cross-reference CD-CH-SW-15 and CD-CH-FW-0 standards.",
        "constraints": "Straight wings | Skew: 0° | Min thickness: 8\" | Cantilever retaining wall design",
        "file_name": "CD-CH-SW0-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-SW0-20.pdf"
    },
    {
        "code": "CH-SW-15",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Straight Wings 15 Skew",
        "summary": "This standard provides engineering drawings for cast-in-place headwalls featuring straight wingwalls at a 15-degree skew. Minimum concrete thickness is specified at 8 inches. Engineers must examine skewed approach channel flow patterns, unequal soil pressures on wingwalls, and structural stability. Connection details mandate reinforced dowel connections, non-shrink grout packings, and positive pipe-to-headwall mechanical ties. Riprap protection must be detailed along the skewed bank interface. Designers should review CD-CH-SW-0 and CD-CH-SW-30 standards.",
        "constraints": "Straight wings | Skew: 15° | Min thickness: 8\" | Skewed soil pressure evaluation",
        "file_name": "CD-CH-SW15-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-SW15-20.pdf"
    },
    {
        "code": "CH-SW-30",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls with Straight Wings 30 Skew",
        "summary": "This standard outlines cast-in-place headwalls with straight wingwalls set at a 30-degree skew. Structural concrete elements require a minimum thickness of 8 inches to handle acute angle stress distributions. Design engineers must review stream alignment, wingwall length requirements, and differential earth loading. Connection details require robust dowel reinforcement, non-shrink grout seals, and mechanical anchoring. Scour protection aprons must be extended across the transition. Engineers should cross-reference CD-CH-SW-15 and CD-CH-FW-30 standards.",
        "constraints": "Straight wings | Skew: 30° | Min thickness: 8\" | Acute angle stress distribution",
        "file_name": "CD-CH-SW30-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-SW30-20.pdf"
    },
    {
        "code": "CH-DW",
        "category": "Headwalls",
        "title": "Cast-In-Place Headwalls Drop Wing Details",
        "summary": "This standard specifies drop wingwall structural details for cast-in-place headwalls used in stepped ditch or sloping terrain culvert installations. Minimum structural concrete thickness is 8 inches. Engineers must evaluate drop height velocities, impact turbulence, and localized scour potential at the drop transition. Connection details require heavy dowelled construction joints tying the drop wing into the main headwall structure, along with positive cutoff walls. Riprap and slope paving must be detailed below the drop. Designers should review all CD-CH series headwall standards.",
        "constraints": "Drop wing configuration | Min thickness: 8\" | Velocity and scour protection",
        "file_name": "CD-CH-DW-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-CH-DW-20.pdf"
    },
    {
        "code": "BCS-20",
        "category": "Box Culverts",
        "title": "Box Culvert Supplemental Wingwalls",
        "summary": "This standard provides supplemental wingwall design and reinforcement details for box culvert extensions and custom angle junctions. Minimum structural wall and footing thickness is 8 inches to 10 inches depending on culvert span. Design engineers must calculate lateral earth pressures, overturning stability, and sliding resistance. Connection details mandate epoxied reinforcing dowels, shear keys, and hydrophilic waterstops tying the supplemental wings into existing barrel structures. Scour protection aprons are required. Engineers should cross-reference CD-XBC and CD-MC series box culvert standards.",
        "constraints": "Supplemental wings | Min thickness: 8\" to 10\" | Overturning and sliding checks",
        "file_name": "CD-BCS-20.dgn",
        "url": "https://ftp.dot.state.tx.us/pub/txdot-info/cmd/cserve/standard/bridge/CD-BCS-20.pdf"
    },
    
]

