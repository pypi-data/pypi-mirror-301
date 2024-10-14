# automatically generated from R1CS.vs2

from libvstruct2 import BigInt, DynExpr, I4, I8, R, VStruct


def store_header(self):
    self.root.FieldSize = self.FieldSize.value
    self.root.nWires = self.nWires.value
    self.root.mConstraints = self.mConstraints.value


class R1CS_WireId2LabelIdSection(VStruct):
    FIELDS = [
        {'name': 'WireLabels', 'count': DynExpr('&root.nWires'), 'type': I8},
    ]


class R1CS_Constraint(VStruct):
    FIELDS = [
        {'name': 'Index', 'type': I4},
        {'name': 'Value', 'type': BigInt, 'length': DynExpr('getattr(&root, "FieldSize", 32)')},
    ]


class R1CS_ConstraintsEntry(VStruct):
    FIELDS = [
        {'name': 'IndexCount', 'type': I4},
        {'name': 'Coefficients', 'count': DynExpr('$IndexCount'), 'type': R1CS_Constraint},
    ]


class R1CS_Constraint(VStruct):
    FIELDS = [
        {'name': 'A', 'type': R1CS_ConstraintsEntry},
        {'name': 'B', 'type': R1CS_ConstraintsEntry},
        {'name': 'C', 'type': R1CS_ConstraintsEntry},
    ]


class R1CS_ConstraintsSection(VStruct):
    FIELDS = [
        {'name': 'Constraints', 'count': DynExpr('&root.mConstraints'), 'type': R1CS_Constraint},
    ]


class R1CS_HeaderSection(VStruct):
    FIELDS = [
        {'name': 'FieldSize', 'type': I4},
        {'name': 'Prime', 'type': BigInt, 'length': DynExpr('$FieldSize')},
        {'name': 'nWires', 'type': I4},
        {'name': 'nPubOut', 'type': I4},
        {'name': 'nPubIn', 'type': I4},
        {'name': 'nPrvIn', 'type': I4},
        {'name': 'nLabels', 'type': I8},
        {'name': 'mConstraints', 'type': I4},
    ]


class R1CS_Section(VStruct):
    FIELDS = [
        {'name': 'Type', 'type': I4},
        {'name': 'Size', 'type': I8},
        {'name': 'Content', 'flags': 1, 'type': R, 'length': DynExpr('$Size')},
        {'name': 'Header', 'flags': 2, 'condition': DynExpr('$Type == 1'), 'type': R1CS_HeaderSection, 'dyn_offset': '@Content', 'post_parse': store_header},
        {'name': 'Constraints', 'flags': 18, 'condition': DynExpr('$Type == 2'), 'type': R1CS_ConstraintsSection, 'dyn_offset': '@Content'},
        {'name': 'LabelMap', 'flags': 2, 'condition': DynExpr('$Type == 3'), 'type': R1CS_WireId2LabelIdSection, 'dyn_offset': '@Content'},
    ]


class R1CS(VStruct):
    ROOT = True
    FILETYPES = ('r1cs',)
    FILTER = '^(r1cs)'
    FIELDS = [
        {'name': 'Magic', 'type': R, 'length': 4, 'validator': b'r1cs'},
        {'name': 'Version', 'type': I4},
        {'name': 'NumSections', 'type': I4},
        {'name': 'Sections', 'count': DynExpr('$NumSections'), 'type': R1CS_Section},
    ]


