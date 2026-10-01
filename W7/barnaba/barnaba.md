# Barnaba
- Github
  - `barnaba ANNOTATE --pdb ../test/data/SARCIN.pdb`
  - 使用了Leontis/Westhof classification

- Literature
  - Annotation:
    - 形成注释首先要求$|\tilde{r}{ij}|$ 和 $|\tilde{r}{ji}|$均小于**1.7Å**

  - Base-pairing:
    - 碱基根据Leontis–Westhof nomenclature分类:
      - [每个碱基有可能形成氢键的点位分布在可在三条边上:](https://en.wikipedia.org/wiki/Non-canonical_base_pairing#:~:text=Each%20nucleobase%20presents%20a%20unique,the%20Hoogsteen%20or%20sugar%20edges)
      - 关于糖苷键在碱基对结合线的同/异侧, 区分顺式/反式
      - ![alt text](image.png)
      - [W/H/S*c/t的18种组合中，有效且具有两个以上氢键的基本几何构型有12种，被Leontis–Westhof定义为12个碱基对“几何族”](https://nakb.org/basics/basepairs.html#:~:text=No,Parallel%20cHH)
    - Barnaba判定为bp的标准
      - **不属于堆叠**的碱基
      - 平面法向夹角 ==$|\theta_{ij}| < 60^\circ$==
      - 存在==至少一个氢键==（至少一对供体-受体距离小于 ==3.3 Å==）
    - Barnaba氢键分类标准($\psi = \arctan2(\hat{y}{ij}, \hat{x}{ij})$)
      - ==Watson-Crick;edge(W): 0.16<ψ≤2.0rad==
      - Hoogsteenedge(H): 2.0<ψ≤4.0rad
      - Sugaredge(S): ψ>4.0rad, ψ≤0.16rad
    - Barnaba的顺反式判断方法
      - 计算两个碱基的糖苷键（连接碱基与核糖）的空间夹角，以判断这对碱基的排列是顺式还是反式

- WC vs WW
  - WW: 任何两碱基通过各自==Watson-Crick边==形成的配对, 不论碱基是否互补 & ==氢键数量>=1==
  - WC: ==正确互补的WWc（RNA中A=U和G≡C配对）==`WWc pairs between complementary bases are called WCc or GUc` & ==氢键数量>=2(AU)/>=3(CG)==
  - 但是：
    1. VMD与Barnaba的统计分类标准并不完全一致，尤其是在手动改变barnaba的参数以后
    2. 可能是由于barnaba的分类不光依赖于氢键，还会考虑碱基，如立体构型等

- 修改界限参数
  - 修改了python源码：
  ```diff {.line-numbers}
  - def annotate(filename,topology=None, stacking_rho_cutoff=2.5, stacking_angle_cutoff=40, pairing_angle_cutoff=60):
  + def annotate(filename,topology=None, stacking_rho_cutoff=2.5, stacking_angle_cutoff=40, pairing_angle_cutoff=60, my_dist_para_input=3.3):

      """
      Find base-pair and base-stacking 

      Parameters
      ----------
      filename : string 
          Filename of structure, any format accepted by MDtraj can be used.
      topology : string, optional
          Topology filename. Must be specified if target is a trajectory.
      stacking_rho_cutoff : float
          Cutoff for base stacking. Rho distance. Default is 2.5 (unit in angstroms).
      stacking_angle_cutoff : float
          Cutoff for base stacking. Angle between the vectors normal to the planes of the two bases. Default is 40 (unit in degrees).
      stacking_angle_cutoff : float
          Cutoff for base pairing. Angle between the vectors normal to the planes of the two bases. Default is 60 (unit in degrees).
  +   my_dist_para_input : float
  +         Number or distances less than  (my_dist_para_input)AA is h_hbonds. Default is 33 (unit in AAs).     
      Returns
      -------
      stackings : list
      pairings : list
          stackings and pairings contains the list of interactions for the N frames in the PDB/trajectory file and it is organized in the following way: for a given frame i=1..n there are k=1..q interactions between residues with index pairings[i][0][k][0] and pairings[i][0][k][1]. The type of interaction is specified at the element pairings[i][1][k].
      seq : 
          List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX       

      """
      
      if(topology==None):
          traj = md.load(filename)
      else:
          traj = md.load(filename,top=topology)

      warn = "# Loading %s \n" % filename
      sys.stderr.write(warn)
      
      return annotate_traj(traj, stacking_rho_cutoff, stacking_angle_cutoff, pairing_angle_cutoff, my_dist_para_input)
  ```
  &
  ```diff {.line-numbers}
  - def annotate_traj(traj, stacking_rho_cutoff=2.5, stacking_angle_cutoff=40, pairing_angle_cutoff=60):
  + def annotate_traj(traj, stacking_rho_cutoff=2.5, stacking_angle_cutoff=40, pairing_angle_cutoff=60, my_dist_para_input=3.3):
  
      # this is the binning for annotation
      bins = [0,1.84,3.84,2.*np.pi]
      bins_label = ["W","H","S"]
      
      top = traj.topology
      # initialize nucleic class
      nn = nucleic.Nucleic(top)
      
      #max_r  = np.max(definitions.f_factors)*1.58
      #condensed_idx =  np.triu_indices(len(nn.ok_residues), 1)

      stackings = []
      pairings = []
      
      for i in range(traj.n_frames):

          # calculate LCS
          coords = traj.xyz[i,nn.indeces_lcs]

          # find bases in close contact (within ellipsoid w radius 1.7)
          pairs,vectors,angles = ff.calc_mat_annotation(coords)
          if(len(pairs)==0):
              stackings.append([[],[]])
              pairings.append([[],[]])
              continue
          
          # calculate rho
          rho_12 = vectors[:,0,0]**2 + vectors[:,0,1]**2
          rho_21 = vectors[:,1,0]**2 + vectors[:,1,1]**2

          # calculate z squared 
          z_12 = vectors[:,0,2]**2
          z_21 = vectors[:,1,2]**2
          # find stacked bases 

          # z_ij  AND z_ji > 2 AA
          stackz_12 = np.where(z_12>0.04)  # nm^2
          stackz_21 = np.where(z_21>0.04)  # nm^2
          
          # rho_ij OR rho_ji < 2.5 AA
          #rhoz_12 =  np.where(rho_12<0.0625)
          #rhoz_21 =  np.where(rho_21<0.0625)
          rhoz_12 =  np.where(rho_12<stacking_rho_cutoff * stacking_rho_cutoff * 0.1 * 0.1)  # nm^2
          rhoz_21 =  np.where(rho_21<stacking_rho_cutoff * stacking_rho_cutoff * 0.1 * 0.1)  # nm^2
          union_rho = np.union1d(rhoz_12[0],rhoz_21[0])

          # angle between normal planes < 40 deg
          #anglez = np.where(np.abs(angles) >0.766)
          anglez = np.where(np.abs(angles) > np.cos(np.radians(stacking_angle_cutoff)))   # cosine of angle beween the normal vectors constructed on base i and base j

          # intersect all criteria
          inter_zeta = np.intersect1d(stackz_12,stackz_21)
          inter_stack = np.intersect1d(union_rho,inter_zeta)
          stacked = np.intersect1d(inter_stack,anglez)

          # now I have found all stackings.
          #stacked_pairs = [[nn.rna_seq[pairs[k,0]],nn.rna_seq[pairs[k,1]]] for k in stacked]
          stacked_pairs = [[pairs[k,0],pairs[k,1]] for k in stacked]
          stacked_annotation = np.chararray((len(stacked_pairs),2), unicode='True')
          stacked_annotation[:] = ">"
          
          # revert where z_ij is negative
          rev1 = np.where(vectors[stacked,0,2]<0)
          stacked_annotation[rev1[0],0] = "<"

          rev2 = np.where(vectors[stacked,1,2]>0)
          stacked_annotation[rev2[0],1] = "<"

          stacked_annotation = ["".join(el) for el in stacked_annotation]
          ######################################################

          # find paired bases  (z_ij < 2 AA AND z_j1 < 2 AA)
          #paired = [j for j in range(len(pairs)) if((j not in stackz_12[0]) and (j not in stackz_21[0]))]
          paired = [j for j in range(len(pairs)) if((j not in stackz_12[0]) or (j not in stackz_21[0]))]
          #paired_pairs = [[nn.rna_seq[pairs[k,0]],nn.rna_seq[pairs[k,1]]] for k in paired]
          paired_pairs = [[pairs[k,0],pairs[k,1]] for k in paired]
          
          # calculate edge angle. subtract 0.16 as Watson edge is not zero
          edge_angles_1 = np.arctan2(vectors[paired,0,1],vectors[paired,0,0]) - definitions.theta1
          edge_angles_2 = np.arctan2(vectors[paired,1,1],vectors[paired,1,0]) - definitions.theta1

          # shift to 0-2pi range
          edge_angles_1[np.where(edge_angles_1<0.0)] += 2.*np.pi
          edge_angles_2[np.where(edge_angles_2<0.0)] += 2.*np.pi

          # find edge: 0 Watson, 1:Hoogsteen, 2sugar
          edge_1 = np.digitize(edge_angles_1,bins)-1
          edge_2 = np.digitize(edge_angles_2,bins)-1

          
          paired_annotation = np.chararray((len(paired_pairs),3), unicode=True)
          paired_annotation[:] = "X"
          
          # now explicit loop, a bit messy. sorry, Guido.
          for j in range(len(paired_pairs)):

              # if angle is larger than 60 deg, skip
              #if(np.abs(angles[paired[j]]) < 0.5 ): continue
              if(np.abs(angles[paired[j]]) < np.cos(np.radians(pairing_angle_cutoff))): continue

              index1 = paired_pairs[j][0]
              index2 = paired_pairs[j][1]
              
              # find donor and acceptor in first base
              r1_donor = nn.donors[index1]
              r1_acceptor = nn.acceptors[index1]
              # find donor and acceptor in second base
              r2_donor = nn.donors[index2]
              r2_acceptor = nn.acceptors[index2]
              combo_list = list(itertools.product(r1_donor,r2_acceptor)) + list(itertools.product(r1_acceptor,r2_donor))
              
              # distances between donor and acceptors
              delta = np.diff(traj.xyz[i,combo_list],axis=1)
              dist_sq = np.sum(delta**2,axis=2)
  -           # number or distances less than  3.3AA is n_hbonds
  -           n_hbonds = (dist_sq<0.1089).sum()

  +           # number or distances less than  dist AA is n_hbonds
  +           my_dist_para_sq = round(my_dist_para_input ** 2 / 100, 4)
  +           n_hbonds = (dist_sq<my_dist_para_sq).sum()

              # if no hydrogen bonds, skip 
              if(n_hbonds==0): continue

              # find edge
              paired_annotation[j][0] = bins_label[edge_1[j]]
              paired_annotation[j][1] = bins_label[edge_2[j]]

              gidxs = [nn.indeces_glyco[index1][1],nn.indeces_glyco[index1][0],nn.indeces_glyco[index2][0],nn.indeces_glyco[index2][1]]

              # if atoms in glyco are missing, do not calculate cis/trans
              if(None in gidxs):
                  paired_annotation[j][2] = "x"
              else:
                  angle_glyco = ff.dihedral(traj.xyz[i,gidxs[0]],traj.xyz[i,gidxs[1]],traj.xyz[i,gidxs[2]],traj.xyz[i,gidxs[3]])
                  if(np.abs(angle_glyco) > 0.5*np.pi):
                      paired_annotation[j][2] = "t"
                  else:
                      paired_annotation[j][2] = "c"
                  
              # if is WWc, check for Watson-crick and GU
              if("".join(paired_annotation[j]) == "WWc"):
                  r1 =  nn.rna_seq_id[index1]
                  r2 =  nn.rna_seq_id[index2]
                  ll = "".join(sorted([r1,r2]))
                  if((z_12[paired[j]] < 0.04) and (z_21[paired[j]]<0.04)):
                      if(((ll=="AU" and n_hbonds > 1) or ( ll == "CG" and n_hbonds > 2))):
                          paired_annotation[j] = ["W","C","c"]
                      if(ll=="GU" and n_hbonds > 1):
                          paired_annotation[j] = ["G","U","c"]
                      
          paired_annotation = ["".join(el) for el in paired_annotation]

          
          stackings.append([stacked_pairs,stacked_annotation])
          pairings.append([paired_pairs,paired_annotation])

      return stackings, pairings, nn.rna_seq

  ```