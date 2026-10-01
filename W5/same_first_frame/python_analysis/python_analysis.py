import mdtraj as md

# 参考结构
ref_file = 'first_frame_340k.gro'
ref = md.load(ref_file)

# 其他温度结构
gro_files = [
    'first_frame_300k.gro',
    'first_frame_320k.gro',
    'first_frame_340k.gro',
    'first_frame_360k.gro',
    # 'first_frame_380k.gro',
    # 'first_frame_400k.gro'
]

# 选定原子（根据实际体系可改为"backbone"、"name P"等）
atom_indices = ref.topology.select('all')  # 或只选主链/磷等

for gro_file in gro_files:
    traj = md.load(gro_file)
    rmsd = md.rmsd(traj, ref, atom_indices=atom_indices)[0]
    print(f"RMSD between {gro_file} and {ref_file}: {rmsd:.4f} nm")
