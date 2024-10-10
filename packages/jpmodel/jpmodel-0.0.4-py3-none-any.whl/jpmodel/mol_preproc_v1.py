import torch
import joblib

import rdkit.Chem as Chem
import rdkit.Chem.AllChem as AllChem

from rdkit.Chem import rdReducedGraphs

class MolFeaturize:

    def __init__ (self, mol, use_pos, clusterer):
        self.mol = mol
        self.clusterer = joblib.load(clusterer)

    def gcn_feature(self):

        mol2 = Chem.RemoveHs(self.mol)
        AllChem.ComputeGasteigerCharges(mol2)
        
        n_bonds = len(mol2.GetBonds())
        n_atoms = len(mol2.GetAtoms())

        node_attr = []
        valid_atoms = {'H': 0, 'C':1, 'N':2, 'O':3, 'F':4, 'P':5, 'S':6, 'Cl':7, 'Br':8, 'I':9}

        for atm_id in range(n_atoms):
            atm = mol2.GetAtomWithIdx(atm_id)

            sym = atm.GetSymbol()
            atm_one_hot = [0] * len(valid_atoms) 
            idx = valid_atoms[sym] 
            atm_one_hot[idx] = 1    

            hybrid = atm.GetHybridization()
            hybrid_one_hot = [0] * 7 
            if hybrid == Chem.HybridizationType.SP3:
                hybrid_one_hot[0] = 1
            elif hybrid == Chem.HybridizationType.SP2:
                hybrid_one_hot[1] = 1
            elif hybrid == Chem.HybridizationType.SP:
                hybrid_one_hot[2] = 1
            elif hybrid == Chem.HybridizationType.S:
                hybrid_one_hot[3] = 1
            elif hybrid == Chem.HybridizationType.SP3D:
                hybrid_one_hot[4] = 1
            elif hybrid == Chem.HybridizationType.SP3D2:
                hybrid_one_hot[5] = 1
            else:
                hybrid_one_hot[6] = 1

            if atm.GetIsAromatic():
                arom = 1
            else:
                arom = 0

            if atm.IsInRing():
                ring_flag = 1
            else:
                ring_flag = 0

            degree_one_hot = [0, 0, 0, 0, 0, 0]
            degree = atm.GetTotalDegree()
            if degree >= 5: 
                degree_one_hot[5]=1
            else:
                degree_one_hot[degree]=1

            num_h = atm.GetTotalNumHs()
            hydrogen_one_hot = [0, 0, 0, 0, 0]
            if num_h >= 4:
                hydrogen_one_hot[4] = 1
            else:
                hydrogen_one_hot[num_h] = 1

            chiral = atm.GetChiralTag()
            if chiral == Chem.rdchem.ChiralType.CHI_OTHER:
                chiral_one_hot = [1, 0, 0, 0]
            elif chiral == Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW:
                chiral_one_hot = [0, 1, 0, 0]
            elif chiral == Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW:
                chiral_one_hot = [0, 0, 1, 0]
            elif chiral == Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                chiral_one_hot = [0, 0, 0, 1]

            exp_valence = atm.GetExplicitValence()
            exp_valence_onehot = [0, 0, 0, 0, 0]
            if exp_valence > 4:
                exp_valence_onehot[4] = 1
            else:
                exp_valence_onehot[exp_valence] = 1

            formal_charge = atm.GetFormalCharge()
            formal_charge_onehot = [0, 0, 0, 0, 0, 0, 0]
            #                      [-, -2, -1, 0, 1, 2, +]
            if formal_charge + 2 < -1:
                formal_charge_onehot[0] = 1
            elif formal_charge + 2 > 4:
                formal_charge_onehot[6] = 1
            else:
                formal_charge_onehot[formal_charge + 2] = 1

            imp_valence = atm.GetImplicitValence()
            imp_valence_onehot = [0, 0, 0, 0, 0]
            if imp_valence > 4:
                imp_valence_onehot[4] = 1
            else:
                imp_valence_onehot[imp_valence] = 1

            total_valence = atm.GetTotalValence()
            total_valence_list = [total_valence]

            partial_charge = [atm.GetDoubleProp("_GasteigerCharge")]

            attr = atm_one_hot +                             hybrid_one_hot +                             degree_one_hot +                             hydrogen_one_hot +                             chiral_one_hot +                             [arom, ring_flag, atm.GetNumRadicalElectrons()] +                             exp_valence_onehot +                             formal_charge_onehot +                             imp_valence_onehot +                             total_valence_list +                             partial_charge

            node_attr.append(attr)
            
        edge_index = []
        edge_attr = []
        edge_weight = []
        for edge_idx in range(n_bonds): 

            bond = mol2.GetBondWithIdx(edge_idx) 
            edge_index.append([bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()])
            edge_index.append([bond.GetEndAtomIdx(), bond.GetBeginAtomIdx()]) 

            btype = bond.GetBondType()
            if btype == Chem.rdchem.BondType.SINGLE:
                    bond_one_hot = [1, 0, 0, 0]
                    edge_weight.extend([1.0])
            elif btype == Chem.rdchem.BondType.AROMATIC:
                    bond_one_hot = [0, 1, 0, 0]
                    edge_weight.extend([1.5])
            elif btype == Chem.rdchem.BondType.DOUBLE:
                    bond_one_hot = [0, 0, 1, 0]
                    edge_weight.extend([2.0])
            elif btype == Chem.rdchem.BondType.TRIPLE:
                    bond_one_hot = [0, 0, 0, 1]
                    edge_weight.extend([3.0])

            stype = bond.GetStereo()
            if stype == Chem.rdchem.BondStereo.STEREOANY:
                stereo_one_hot = [1, 0, 0, 0, 0, 0]
            elif stype == Chem.rdchem.BondStereo.STEREOCIS:
                stereo_one_hot = [0, 1, 0, 0, 0, 0]
            elif stype == Chem.rdchem.BondStereo.STEREOE:
                stereo_one_hot = [0, 0, 1, 0, 0, 0]
            elif stype == Chem.rdchem.BondStereo.STEREONONE:
                stereo_one_hot = [0, 0, 0, 1, 0, 0]
            elif stype == Chem.rdchem.BondStereo.STEREOTRANS:
                stereo_one_hot = [0, 0, 0, 0, 1, 0]
            elif stype == Chem.rdchem.BondStereo.STEREOZ:
                stereo_one_hot = [0, 0, 0, 0, 0, 1]

            if bond.IsInRing():
                ring_bond = 1
            else:
                ring_bond = 0

            if bond.GetIsConjugated():
                conjugate = 1
            else:
                conjugate = 0

            attr = bond_one_hot + stereo_one_hot + [ring_bond, conjugate] 

            edge_attr.append(attr)
            edge_attr.append(attr)

        edge_attr = torch.tensor(edge_attr, dtype = torch.float)
        node_attr = torch.tensor(node_attr, dtype = torch.float)
        edge_index = torch.tensor(edge_index, dtype = torch.long)
        edge_index = edge_index.t().contiguous()
        edge_weight = torch.tensor(edge_weight, dtype = torch.float)

        if self.use_pos: # optional
            val = AllChem.EmbedMolecule(mol2)
            if val !=0:
                print(f"Error while generating 3D: {Chem.MolToSmiles(self.mol)}")
                return None

            pos_list = [] 
            for atm_id in range(n_atoms):
                atm_pos = mol2.GetConformer(0).GetAtomPosition(atm_id)
                crd = [atm_pos.x, atm_pos.y, atm_pos.z]
                pos_list.append(crd)

            pos = torch.tensor(pos_list, dtype=torch.float)
        else:
            pos = None

        return edge_index, node_attr, edge_attr, pos, edge_weight

    def ecfp_feature(self, bits=1024):

        ecfp = AllChem.GetMorganFingerprintAsBitVect(self.mol, radius=2, nBits=bits).ToList()

        cluster_vector = [0] * 10
        cluster_vector[self.clusterer.predict([AllChem.GetMorganFingerprintAsBitVect(self.mol, radius=2, nBits=2048).ToList()])[0]] = 1
        cluster_vector = torch.tensor(cluster_vector, dtype=torch.float32).view(1, 10)

        ergfp = rdReducedGraphs.GetErGFingerprint(self.mol).tolist()

        apfp = Chem.rdMolDescriptors.GetHashedAtomPairFingerprint(self.mol, bits, use2D=True).ToList()

        rdkgen = Chem.rdFingerprintGenerator.GetRDKitFPGenerator(fpSize=1024)
        rdkfp = rdkgen.GetFingerprint(self.mol).ToList()

        features = ergfp + rdkfp + ecfp + apfp
        features = torch.tensor(features, dtype=torch.float32).view(1, len(features))

        return features, cluster_vector
