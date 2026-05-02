"""
ICT Policy Knowledge Network Analysis
Knowledge, Networks, and Power in Global Education Governance
Sub-Saharan Africa / Cameroon Case

PhD Research Proposal Pilot Study
For: Geneva Graduate Institute - SNSF Project on Knowledge Production in Global Education Governance

Methodology: Social Network Analysis (SNA) + Network-Cued Interviews
Author: NANJE PATRICK ITARNGOH
Date: April 2026
"""

import warnings
warnings.filterwarnings('ignore')

# Import required packages
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    import numpy as np
    print("✓ Packages loaded successfully")
except ImportError as e:
    print(f"Error importing packages: {e}")
    print("\nPlease install required packages:")
    print("pip install networkx matplotlib numpy")
    exit(1)

# Import pandas if available
try:
    import pandas as pd
    HAS_PANDAS = True
    print("✓ Pandas loaded successfully")
except ImportError:
    HAS_PANDAS = False
    print("⚠ Pandas not available - will use basic Python instead")
    print("  (Install with: pip install pandas)")

# Import community detection module
try:
    from networkx.algorithms.community import greedy_modularity_communities
    HAS_COMMUNITY = True
    print("✓ Community detection module loaded successfully")
except ImportError:
    HAS_COMMUNITY = False
    print("⚠ Community detection not available")
    print("  (This is part of NetworkX core - should be available)")

print("\n" + "=" * 80)
print("ICT POLICY KNOWLEDGE NETWORK ANALYSIS")
print("Research: Knowledge, Networks, and Power in Global Education Governance")
print("=" * 80 + "\n")

# ============================================================================
# 1. CONSTRUCT THE POLICY NETWORK
# ============================================================================

print("Building policy network...")

# Create directed graph
G = nx.DiGraph()

# Define actors with their attributes 
actor_names = [
    # Global International Organisations (IOs) - Core knowledge producers
    "UNESCO_HQ", "World_Bank_Edu", "World_Bank_EdTech", "OECD_CERI", "OECD_EDU_ICT", "ITU",
    # Regional IOs - Intermediaries
    "UNESCO_BREDA", "AU_PanAf",
    # National Ministries - Policy receivers/enactors
    "MINEDUB_Cameroon", "MINESEC_Cameroon", "MoE_Kenya", "MoE_Rwanda",
    # Teacher Education Institutions - Local mediators
    "ENS_Yaounde", "ENS_Bamenda", "TTI_Thika", "UR_CE",
    # Pedagogical Inspectorates - Enactment monitors
    "Ped_Inspectorate_Cam", "Ped_Inspectorate_Kenya",
    # Consultants - Knowledge brokers
    "Consultant_Global", "Consultant_Local1", "Consultant_Local2"
]

actor_types = [
    "IO_Global", "IO_Global", "IO_Global", "IO_Global", "IO_Global", "IO_Global",
    "IO_Regional", "IO_Regional",
    "Ministry", "Ministry", "Ministry", "Ministry",
    "Teacher_Edu", "Teacher_Edu", "Teacher_Edu", "Teacher_Edu",
    "Inspectorate", "Inspectorate",
    "Consultant", "Consultant", "Consultant"
]

actor_locations = [
    "Global_North", "Global_North", "Global_North", "Global_North", "Global_North", "Global_North",
    "Regional", "Regional",
    "SSA", "SSA", "SSA", "SSA",
    "SSA", "SSA", "SSA", "SSA",
    "SSA", "SSA",
    "Mixed", "Mixed", "Mixed"
]

# Add nodes to graph
for i, name in enumerate(actor_names):
    G.add_node(name, type=actor_types[i], location=actor_locations[i])

print(f"✓ Added {len(actor_names)} nodes to network")

# Define edges (from, to, relation)
edge_list = [
    # ========== KNOWLEDGE PRODUCTION (Co-authorship & Collaboration) ==========
    ("UNESCO_HQ", "Consultant_Global", "co_authorship"),
    ("UNESCO_HQ", "OECD_CERI", "co_authorship"),
    ("UNESCO_HQ", "OECD_EDU_ICT", "co_authorship"),
    ("World_Bank_Edu", "Consultant_Global", "co_authorship"),
    ("World_Bank_Edu", "World_Bank_EdTech", "co_authorship"),
    ("World_Bank_EdTech", "OECD_EDU_ICT", "co_authorship"),
    ("OECD_CERI", "UNESCO_HQ", "co_authorship"),
    ("OECD_EDU_ICT", "UNESCO_HQ", "co_authorship"),
    ("OECD_EDU_ICT", "OECD_CERI", "co_authorship"),
    
    # ========== STANDARD SETTING & POLICY FRAMEWORKS ==========
    # UNESCO ICT Framework
    ("UNESCO_HQ", "ITU", "standard_setting"),
    ("ITU", "AU_PanAf", "standard_setting"),
    ("AU_PanAf", "UNESCO_BREDA", "regional_coordination"),
    
    # World Bank EdTech Strategy
    ("World_Bank_EdTech", "ITU", "standard_setting"),
    ("World_Bank_EdTech", "Consultant_Global", "policy_development"),
    
    # OECD Digital Education
    ("OECD_EDU_ICT", "ITU", "standard_setting"),
    ("OECD_EDU_ICT", "UNESCO_BREDA", "dissemination"),
    
    # ========== DISSEMINATION TO REGIONAL BODIES ==========
    ("UNESCO_HQ", "UNESCO_BREDA", "dissemination"),
    ("World_Bank_Edu", "UNESCO_BREDA", "dissemination"),
    ("OECD_CERI", "UNESCO_BREDA", "dissemination"),
    ("World_Bank_EdTech", "UNESCO_BREDA", "dissemination"),
    
    # ========== CAPACITY BUILDING & POLICY ADVICE (Global → Regional → National) ==========
    ("UNESCO_BREDA", "MINEDUB_Cameroon", "capacity_building"),
    ("UNESCO_BREDA", "MINESEC_Cameroon", "capacity_building"),
    ("UNESCO_BREDA", "MoE_Kenya", "capacity_building"),
    ("AU_PanAf", "MoE_Kenya", "policy_advice"),
    ("AU_PanAf", "MoE_Rwanda", "policy_advice"),
    ("World_Bank_Edu", "MoE_Rwanda", "policy_advice"),
    ("World_Bank_Edu", "MINEDUB_Cameroon", "funding"),
    ("World_Bank_EdTech", "MINEDUB_Cameroon", "policy_advice"),
    ("World_Bank_EdTech", "MoE_Kenya", "funding"),
    ("OECD_EDU_ICT", "MINEDUB_Cameroon", "policy_advice"),
    
    # ========== NATIONAL POLICY INTERPRETATION ==========
    ("MINEDUB_Cameroon", "Ped_Inspectorate_Cam", "policy_interpretation"),
    ("MINESEC_Cameroon", "Ped_Inspectorate_Cam", "policy_interpretation"),
    ("MINEDUB_Cameroon", "Consultant_Local1", "consultancy"),
    ("MoE_Kenya", "Ped_Inspectorate_Kenya", "policy_interpretation"),
    ("MoE_Rwanda", "Consultant_Local2", "consultancy"),
    
    # ========== TRAINING AND MEDIATION (National → Teacher Education) ==========
    ("MINEDUB_Cameroon", "ENS_Yaounde", "training"),
    ("Ped_Inspectorate_Cam", "ENS_Yaounde", "training"),
    ("Ped_Inspectorate_Cam", "ENS_Bamenda", "training"),
    ("MoE_Kenya", "TTI_Thika", "training"),
    ("MoE_Rwanda", "UR_CE", "training"),
    
    # ========== MONITORING AND FEEDBACK (Enactment → Policy) ==========
    ("ENS_Yaounde", "Ped_Inspectorate_Cam", "monitoring"),
    ("ENS_Bamenda", "Ped_Inspectorate_Cam", "monitoring"),
    ("TTI_Thika", "Ped_Inspectorate_Kenya", "monitoring"),
    
    # ========== FEEDBACK LOOPS (Local → Global) - CRITICAL FOR ENACTMENT THEORY ==========
    ("ENS_Yaounde", "UNESCO_BREDA", "feedback"),
    ("Ped_Inspectorate_Cam", "Consultant_Global", "mediation_report"),
    ("MINEDUB_Cameroon", "World_Bank_Edu", "negotiation"),
    ("MINEDUB_Cameroon", "World_Bank_EdTech", "negotiation"),
    ("Ped_Inspectorate_Kenya", "UNESCO_BREDA", "feedback"),
    ("MoE_Rwanda", "OECD_EDU_ICT", "feedback"),
    
    # ========== CONSULTANT NETWORKS (Horizontal Knowledge Flow) ==========
    ("Consultant_Global", "Consultant_Local2", "consultancy"),
    ("Consultant_Local1", "MINEDUB_Cameroon", "consultancy"),
    ("Consultant_Global", "ENS_Yaounde", "policy_adaptation"),
    ("MINEDUB_Cameroon", "Consultant_Global", "mediation"),
    ("Consultant_Global", "Ped_Inspectorate_Cam", "technical_assistance"),
    ("Consultant_Local2", "MoE_Rwanda", "consultancy"),
    
    # ========== CROSS-COUNTRY LEARNING ==========
    ("MINEDUB_Cameroon", "MoE_Kenya", "south_south_cooperation"),
    ("ENS_Yaounde", "TTI_Thika", "peer_learning")
]

# Add edges to graph
for src, tgt, relation in edge_list:
    G.add_edge(src, tgt, relation=relation)

print(f"✓ Added {len(edge_list)} edges to network")
print(f"\nNetwork summary:")
print(f"  - Nodes: {G.number_of_nodes()}")
print(f"  - Edges: {G.number_of_edges()}")
print(f"  - Network density: {nx.density(G):.4f}")
print(f"  - Reciprocity: {nx.reciprocity(G):.4f}")

# ============================================================================
# 2. CENTRALITY ANALYSIS (RQ1 & RQ2)
# ============================================================================

print("\n" + "=" * 80)
print("RQ1 & RQ2: KEY ACTORS AND NETWORK STRUCTURE")
print("=" * 80)

# Calculate centrality measures
in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())
total_degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G, normalized=True)

# Calculate eigenvector centrality (influence)
try:
    eigenvector = nx.eigenvector_centrality_numpy(G)
except:
    # Fallback for directed graphs - convert to undirected
    eigenvector = nx.eigenvector_centrality_numpy(G.to_undirected())
    print("  (Note: Used undirected graph for eigenvector centrality)")

# Create results list
results = []
for node in G.nodes():
    results.append({
        'Actor': node,
        'Type': G.nodes[node]['type'],
        'Location': G.nodes[node]['location'],
        'InDegree': in_degree[node],
        'OutDegree': out_degree[node],
        'TotalDegree': total_degree[node],
        'Betweenness': round(betweenness[node], 4),
        'Eigenvector': round(eigenvector.get(node, 0), 4)
    })

# Sort by betweenness
results_sorted = sorted(results, key=lambda x: x['Betweenness'], reverse=True)

print("\n📊 TOP 10 ACTORS BY BETWEENNESS CENTRALITY (Brokerage Power):")
print("-" * 110)
print(f"{'Actor':<22} {'Type':<14} {'Location':<12} {'In':<4} {'Out':<5} {'Betweenness':<12} {'Eigenvector':<10}")
print("-" * 110)
for r in results_sorted[:10]:
    print(f"{r['Actor']:<22} {r['Type']:<14} {r['Location']:<12} {r['InDegree']:<4} {r['OutDegree']:<5} {r['Betweenness']:<12.4f} {r['Eigenvector']:<10.4f}")

print("\n📊 TOP 5 BY IN-DEGREE (Knowledge Receivers - Legitimised Expertise):")
results_by_indegree = sorted(results, key=lambda x: x['InDegree'], reverse=True)
print("-" * 100)
print(f"{'Actor':<22} {'Type':<14} {'Location':<12} {'InDegree':<10}")
print("-" * 100)
for r in results_by_indegree[:5]:
    print(f"{r['Actor']:<22} {r['Type']:<14} {r['Location']:<12} {r['InDegree']:<10}")

print("\n📊 TOP 5 BY OUT-DEGREE (Knowledge Producers):")
results_by_outdegree = sorted(results, key=lambda x: x['OutDegree'], reverse=True)
print("-" * 100)
print(f"{'Actor':<22} {'Type':<14} {'Location':<12} {'OutDegree':<10}")
print("-" * 100)
for r in results_by_outdegree[:5]:
    print(f"{r['Actor']:<22} {r['Type']:<14} {r['Location']:<12} {r['OutDegree']:<10}")

print("\n📊 TOP 5 BY EIGENVECTOR CENTRALITY (Overall Influence):")
results_by_eigen = sorted(results, key=lambda x: x['Eigenvector'], reverse=True)
print("-" * 100)
print(f"{'Actor':<22} {'Type':<14} {'Location':<12} {'Eigenvector':<10}")
print("-" * 100)
for r in results_by_eigen[:5]:
    print(f"{r['Actor']:<22} {r['Type']:<14} {r['Location']:<12} {r['Eigenvector']:<10.4f}")

# ============================================================================
# 3. BROKERAGE ANALYSIS (Gould-Fernandez)
# ============================================================================

print("\n" + "=" * 80)
print("GOULD-FERNANDEZ BROKERAGE ANALYSIS")
print("Identifies actors who connect otherwise disconnected groups")
print("=" * 80)

def identify_brokers(G):
    """
    Identify brokers using Gould-Fernandez brokerage role concept.
    A broker connects predecessors to successors, facilitating flow between groups.
    """
    brokerage = {}
    for node in G.nodes():
        # Count how many pairs this node connects
        predecessors = set(G.predecessors(node))
        successors = set(G.successors(node))
        # Broker connects two otherwise unconnected groups
        # Higher score = more brokerage opportunities
        brokerage[node] = len(predecessors) * len(successors)
    return brokerage

broker_scores = identify_brokers(G)
print("\n📊 TOP 10 BROKERS (Gould-Fernandez Score):")
print("-" * 80)
print(f"{'Actor':<22} {'Type':<14} {'Brokerage_Score':<15}")
print("-" * 80)
for node, score in sorted(broker_scores.items(), key=lambda x: x[1], reverse=True)[:10]:
    node_type = G.nodes[node]['type']
    print(f"{node:<22} {node_type:<14} {score:<15}")

# ============================================================================
# 4. COMMUNITY DETECTION (Clustering Analysis)
# ============================================================================

print("\n" + "=" * 80)
print("COMMUNITY DETECTION (Modularity Analysis)")
print("Identifies epistemic clusters within the network")
print("=" * 80)

if HAS_COMMUNITY:
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()
    communities = list(greedy_modularity_communities(G_undirected))
    
    print(f"\n📊 Detected {len(communities)} epistemic communities:")
    for i, comm in enumerate(communities):
        comm_names = [n.split('_')[0] if '_' in n else n for n in sorted(comm)]
        print(f"\n  Community {i+1}: {', '.join(comm_names[:8])}")
        if len(comm) > 8:
            print(f"             ... and {len(comm)-8} more")
    
    # Calculate modularity
    modularity = nx.community.modularity(G_undirected, communities)
    print(f"\n📊 Network Modularity: {modularity:.4f}")
    if modularity > 0.3:
        print("    → Strong community structure: Knowledge is clustered by geography/organisation")
    else:
        print("    → Weak community structure: Knowledge flows across clusters")
else:
    print("\n  ⚠ Community detection skipped (module not available)")

# ============================================================================
# 5. POWER ANALYSIS - GLOBAL NORTH VS SSA (RQ4)
# ============================================================================

print("\n" + "=" * 80)
print("RQ4: POWER RELATIONS - Global North vs Sub-Saharan Africa")
print("=" * 80)

# Calculate statistics by location
location_stats = {}
locations = set(r['Location'] for r in results)

for loc in locations:
    loc_results = [r for r in results if r['Location'] == loc]
    if loc_results:
        location_stats[loc] = {
            'count': len(loc_results),
            'mean_betweenness': np.mean([r['Betweenness'] for r in loc_results]),
            'mean_indegree': np.mean([r['InDegree'] for r in loc_results]),
            'mean_outdegree': np.mean([r['OutDegree'] for r in loc_results]),
            'mean_eigenvector': np.mean([r['Eigenvector'] for r in loc_results]),
            'total_outdegree': sum([r['OutDegree'] for r in loc_results]),
            'total_indegree': sum([r['InDegree'] for r in loc_results])
        }

print("\n📊 Centrality Measures by Geopolitical Location:")
print("-" * 80)
for loc, stats in sorted(location_stats.items()):
    print(f"\n{loc}:")
    print(f"  - Number of actors: {stats['count']}")
    print(f"  - Mean betweenness: {stats['mean_betweenness']:.4f}")
    print(f"  - Mean in-degree: {stats['mean_indegree']:.2f}")
    print(f"  - Mean out-degree: {stats['mean_outdegree']:.2f}")
    print(f"  - Mean eigenvector: {stats['mean_eigenvector']:.4f}")
    print(f"  - Total knowledge output (out-degree): {stats['total_outdegree']}")
    print(f"  - Total knowledge input (in-degree): {stats['total_indegree']}")

# Calculate power concentration indices
in_cent_values = list(nx.in_degree_centrality(G).values())
max_in_cent = max(in_cent_values)
n_nodes = G.number_of_nodes()
in_centralization_index = (sum(in_cent_values) - max_in_cent) / (n_nodes - 1) if n_nodes > 1 else 0

out_cent_values = list(nx.out_degree_centrality(G).values())
max_out_cent = max(out_cent_values)
out_centralization_index = (sum(out_cent_values) - max_out_cent) / (n_nodes - 1) if n_nodes > 1 else 0

between_cent_values = list(betweenness.values())
max_between_cent = max(between_cent_values)
between_centralization_index = (sum(between_cent_values) - max_between_cent) / (n_nodes - 1) if n_nodes > 1 else 0

print(f"\n📊 Network Power Concentration Indices:")
print(f"  - In-degree centralization: {in_centralization_index:.4f}")
print(f"  - Out-degree centralization: {out_centralization_index:.4f}")
print(f"  - Betweenness centralization: {between_centralization_index:.4f}")
if in_centralization_index > 0.5:
    print("    → High concentration: Knowledge reception is centralized in few actors")
else:
    print("    → Moderate concentration: Knowledge reception is relatively distributed")

# Calculate Global North vs SSA control
global_north_out = location_stats.get('Global_North', {}).get('total_outdegree', 0)
global_north_in = location_stats.get('Global_North', {}).get('total_indegree', 0)
ssa_out = location_stats.get('SSA', {}).get('total_outdegree', 0)
ssa_in = location_stats.get('SSA', {}).get('total_indegree', 0)
total_out_all = global_north_out + ssa_out
total_in_all = global_north_in + ssa_in

if total_out_all > 0:
    global_north_control_out = (global_north_out / total_out_all) * 100
    ssa_control_out = (ssa_out / total_out_all) * 100
    print(f"\n📊 Knowledge Production Control (Out-Degree):")
    print(f"  - Global North actors produce {global_north_control_out:.1f}% of all knowledge outputs")
    print(f"  - SSA actors produce {ssa_control_out:.1f}%")
    print(f"  → Global North produces {global_north_control_out/ssa_control_out:.1f}x more knowledge")

if total_in_all > 0:
    global_north_control_in = (global_north_in / total_in_all) * 100
    ssa_control_in = (ssa_in / total_in_all) * 100
    print(f"\n📊 Knowledge Reception Control (In-Degree):")
    print(f"  - Global North actors receive {global_north_control_in:.1f}% of knowledge")
    print(f"  - SSA actors receive {ssa_control_in:.1f}%")
    print(f"  → SSA receives {ssa_control_in/global_north_control_in:.1f}x more knowledge than Global North")
    print(f"    (Indicates dependency: SSA is primarily a knowledge receiver)")

# ============================================================================
# 6. MID-LEVEL ACTORS MEDIATION (RQ3)
# ============================================================================

print("\n" + "=" * 80)
print("RQ3: POLICY ENACTMENT - Role of Mid-Level Actors")
print("Actors who mediate between global policy and local practice")
print("=" * 80)

mediator_types = ['Inspectorate', 'Teacher_Edu']
mediators = [r for r in results if r['Type'] in mediator_types]
mediators_sorted = sorted(mediators, key=lambda x: x['Betweenness'], reverse=True)

print("\n📊 Mid-Level Actors (Inspectorate & Teacher Educators):")
print("-" * 90)
if mediators_sorted:
    print(f"{'Actor':<22} {'Type':<14} {'Betweenness':<12} {'InDegree':<8} {'OutDegree':<8} {'Eigenvector':<10}")
    print("-" * 90)
    for r in mediators_sorted:
        print(f"{r['Actor']:<22} {r['Type']:<14} {r['Betweenness']:<12.4f} {r['InDegree']:<8} {r['OutDegree']:<8} {r['Eigenvector']:<10.4f}")
else:
    print("  No mediator actors found")

# Compare mediator vs non-mediator betweenness
mediator_betweenness = np.mean([r['Betweenness'] for r in mediators]) if mediators else 0
non_mediators = [r for r in results if r['Type'] not in mediator_types and r['Type'] not in ['IO_Global', 'IO_Regional']]
non_mediator_betweenness = np.mean([r['Betweenness'] for r in non_mediators]) if non_mediators else 0

if non_mediator_betweenness > 0:
    ratio = mediator_betweenness / non_mediator_betweenness
    print(f"\n📊 Mediation Power Comparison:")
    print(f"  - Average betweenness (mediators): {mediator_betweenness:.4f}")
    print(f"  - Average betweenness (non-mediators within SSA): {non_mediator_betweenness:.4f}")
    print(f"  - Mediators are {ratio:.1f}x more central as brokers")
    if ratio > 1.5:
        print("    → Strong evidence: Mid-level actors are critical policy mediators")

# ============================================================================
# 7. KNOWLEDGE FLOW PATHS
# ============================================================================

print("\n" + "=" * 80)
print("KNOWLEDGE CIRCULATION PATHS")
print("Tracing how policy knowledge travels from IOs to national actors")
print("=" * 80)

# Identify global IOs and SSA actors
global_ios = [r['Actor'] for r in results if r['Type'] == 'IO_Global']
ssa_actors = [r['Actor'] for r in results if r['Location'] == 'SSA']

print(f"\n📊 Knowledge Flow from Global IOs to SSA Actors:")
print(f"  Global IOs: {', '.join([io.split('_')[0] for io in global_ios])}")
print(f"  SSA Actors: {len(ssa_actors)} actors")

paths_found = 0
all_path_lengths = []

for source in global_ios[:3]:  # Limit to top 3 global IOs for readability
    print(f"\n  From {source.split('_')[0]}:")
    for target in ssa_actors[:5]:  # Show first 5 SSA actors
        if nx.has_path(G, source, target):
            path = nx.shortest_path(G, source, target)
            path_length = nx.shortest_path_length(G, source, target)
            all_path_lengths.append(path_length)
            print(f"    → {target} (distance: {path_length} steps)")
            print(f"       {' → '.join([p.split('_')[0] if '_' in p else p for p in path])}")
            paths_found += 1
        else:
            print(f"    → {target}: No direct path found")

# Calculate average path length
if all_path_lengths:
    avg_path = np.mean(all_path_lengths)
    print(f"\n📊 Average knowledge flow distance: {avg_path:.2f} steps from Global IO to SSA")
    print(f"   (Based on {len(all_path_lengths)} paths)")

# Identify structural holes (gaps in network)
print(f"\n📊 Structural Holes Analysis:")
print(f"  - Network density: {nx.density(G):.4f} (low density = many structural holes)")
print(f"  - Actors with high betweenness fill structural holes")
print(f"  - Top hole-fillers: {results_sorted[0]['Actor']}, {results_sorted[1]['Actor']}, {results_sorted[2]['Actor']}")

# ============================================================================
# 8. NETWORK VISUALISATION
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING NETWORK VISUALISATION")
print("=" * 80)

# Define colours for actor types
colour_map = {
    'IO_Global': '#E41A1C',      # Red
    'IO_Regional': '#377EB8',    # Blue
    'Ministry': '#4DAF4A',       # Green
    'Teacher_Edu': '#984EA3',    # Purple
    'Inspectorate': '#FF7F00',   # Orange
    'Consultant': '#F5C542'      # Gold
}

# Prepare node colours and sizes
node_colours = []
node_sizes = []
for node in G.nodes():
    node_colours.append(colour_map.get(G.nodes[node]['type'], '#CCCCCC'))
    # Scale node size by betweenness (min 300, max 2500)
    size = betweenness[node] * 3000 + 500
    node_sizes.append(size)

# Layout for visualisation
pos = nx.spring_layout(G, k=1.8, seed=42, iterations=50)

# Create figure
plt.figure(figsize=(18, 14))

# Draw edges with different styles based on relation type
edge_colors = []
for u, v, data in G.edges(data=True):
    rel = data.get('relation', 'unknown')
    if rel in ['co_authorship', 'standard_setting', 'policy_development']:
        edge_colors.append('#1a1a1a')  # Dark grey - production
    elif rel in ['dissemination', 'capacity_building', 'policy_advice']:
        edge_colors.append('#4d4d4d')  # Medium grey - transmission
    elif rel in ['feedback', 'negotiation', 'mediation_report']:
        edge_colors.append('#999999')  # Light grey - feedback
    else:
        edge_colors.append('#cccccc')  # Very light grey - other

nx.draw_networkx_edges(G, pos, edge_color=edge_colors, alpha=0.5, 
                       arrows=True, arrowsize=8, arrowstyle='->', width=1.2)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color=node_colours, 
                       node_size=node_sizes, alpha=0.9, edgecolors='black', linewidths=1.5)

# Draw labels (wrap long names)
labels = {}
for node in G.nodes():
    if len(node) > 15:
        parts = node.split('_')
        if len(parts) > 1:
            if node == "Ped_Inspectorate_Cam":
                labels[node] = "Ped.\nInspectorate\nCameroon"
            elif node == "Ped_Inspectorate_Kenya":
                labels[node] = "Ped.\nInspectorate\nKenya"
            else:
                labels[node] = parts[0] + '\n' + '_'.join(parts[1:])
        else:
            labels[node] = node
    else:
        if node == "Consultant_Global":
            labels[node] = "Consultant\nGlobal"
        elif node == "MINEDUB_Cameroon":
            labels[node] = "MINEDUB\nCameroon"
        elif node == "MINESEC_Cameroon":
            labels[node] = "MINESEC\nCameroon"
        else:
            labels[node] = node

nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_weight='bold')

plt.title("ICT Policy Knowledge Network: Production, Circulation, and Mediation\nUNESCO, OECD, and World Bank in Sub-Saharan Africa (Cameroon Focus)", 
          fontsize=14, fontweight='bold', pad=20)
plt.axis('off')

# Create legend
legend_elements = [Patch(facecolor=colour_map[t], label=t, alpha=0.9, edgecolor='black') 
                   for t in colour_map.keys()]
edge_legend = [
    Patch(facecolor='#1a1a1a', label='Knowledge Production', alpha=0.7),
    Patch(facecolor='#4d4d4d', label='Transmission/Dissemination', alpha=0.7),
    Patch(facecolor='#999999', label='Feedback/Negotiation', alpha=0.7)
]
plt.legend(handles=legend_elements + edge_legend, loc='upper left', bbox_to_anchor=(1, 1), 
           title="Actor Type & Edge Type", title_fontsize=12, fontsize=9)

plt.tight_layout()
plt.savefig('ict_policy_network.png', dpi=300, bbox_inches='tight', facecolor='white')
print("\n✓ Visualisation saved as 'ict_policy_network.png'")

plt.show()

# ============================================================================
# 9. EGO-NETWORKS FOR INTERVIEW CUES
# ============================================================================

print("\n" + "=" * 80)
print("EGO-NETWORKS FOR NETWORK-CUED INTERVIEWS")
print("=" * 80)

key_actors = ["MINEDUB_Cameroon", "UNESCO_BREDA", "Ped_Inspectorate_Cam", "Consultant_Global"]

for ego_name in key_actors:
    if ego_name in G.nodes():
        ego_net = list(nx.ego_graph(G, ego_name, radius=1).nodes())
        print(f"\n📋 Ego-network for {ego_name}:")
        print(f"   Direct connections ({len(ego_net)-1}):")
        for neighbor in ego_net:
            if neighbor != ego_name:
                edge_data = G.get_edge_data(ego_name, neighbor) or G.get_edge_data(neighbor, ego_name)
                relation = edge_data.get('relation', 'unknown') if edge_data else 'unknown'
                direction = "→" if G.has_edge(ego_name, neighbor) else "←" if G.has_edge(neighbor, ego_name) else "↔"
                print(f"     {direction} {neighbor} ({relation})")

# ============================================================================
# 10. EXPORT DATA FOR QUALITATIVE ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("EXPORTING DATA FOR QUALITATIVE ANALYSIS")
print("=" * 80)

# Export to GraphML for Gephi
try:
    nx.write_graphml(G, "ict_policy_network.graphml")
    print("✓ Network exported to 'ict_policy_network.graphml'")
    print("  (Can be opened with Gephi for advanced visualisation)")
except Exception as e:
    print(f"⚠ Could not export GraphML: {e}")

# Export centrality data
if HAS_PANDAS:
    try:
        df = pd.DataFrame(results)
        df.to_csv("centrality_measures.csv", index=False)
        print("✓ Centrality data exported to 'centrality_measures.csv'")
    except Exception as e:
        print(f"⚠ Could not export CSV: {e}")
else:
    try:
        with open("centrality_measures.txt", "w") as f:
            f.write("Actor,Type,Location,InDegree,OutDegree,TotalDegree,Betweenness,Eigenvector\n")
            for r in results:
                f.write(f"{r['Actor']},{r['Type']},{r['Location']},{r['InDegree']},{r['OutDegree']},{r['TotalDegree']},{r['Betweenness']},{r['Eigenvector']}\n")
        print("✓ Centrality data exported to 'centrality_measures.txt'")
    except Exception as e:
        print(f"⚠ Could not export text file: {e}")

# Export edge list for further analysis
try:
    edge_data = []
    for u, v, data in G.edges(data=True):
        edge_data.append({
            'Source': u,
            'Target': v,
            'Relation': data.get('relation', 'unknown')
        })
    
    if HAS_PANDAS:
        df_edges = pd.DataFrame(edge_data)
        df_edges.to_csv("edge_list.csv", index=False)
        print("✓ Edge list exported to 'edge_list.csv'")
    else:
        with open("edge_list.txt", "w") as f:
            f.write("Source,Target,Relation\n")
            for e in edge_data:
                f.write(f"{e['Source']},{e['Target']},{e['Relation']}\n")
        print("✓ Edge list exported to 'edge_list.txt'")
except Exception as e:
    print(f"⚠ Could not export edge list: {e}")

# Export broker scores
