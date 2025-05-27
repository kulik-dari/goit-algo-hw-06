graph [
  node [
    id 0
    label "&#1062;&#1077;&#1085;&#1090;&#1088;&#1072;&#1083;&#1100;&#1085;&#1072; &#1087;&#1083;&#1086;&#1097;&#1072;"
    district "&#1062;&#1077;&#1085;&#1090;&#1088;"
    type "metro"
    population 50000
  ]
  node [
    id 1
    label "&#1058;&#1077;&#1072;&#1090;&#1088;&#1072;&#1083;&#1100;&#1085;&#1072;"
    district "&#1062;&#1077;&#1085;&#1090;&#1088;"
    type "metro"
    population 30000
  ]
  node [
    id 2
    label "&#1059;&#1085;&#1110;&#1074;&#1077;&#1088;&#1089;&#1080;&#1090;&#1077;&#1090;"
    district "&#1062;&#1077;&#1085;&#1090;&#1088;"
    type "metro"
    population 40000
  ]
  node [
    id 3
    label "&#1055;&#1110;&#1074;&#1085;&#1110;&#1095;&#1085;&#1080;&#1081; &#1074;&#1086;&#1082;&#1079;&#1072;&#1083;"
    district "&#1055;&#1110;&#1074;&#1085;&#1110;&#1095;"
    type "train"
    population 35000
  ]
  node [
    id 4
    label "&#1054;&#1079;&#1077;&#1088;&#1085;&#1072;"
    district "&#1055;&#1110;&#1074;&#1085;&#1110;&#1095;"
    type "bus"
    population 25000
  ]
  node [
    id 5
    label "&#1051;&#1110;&#1089;&#1086;&#1087;&#1072;&#1088;&#1082;"
    district "&#1055;&#1110;&#1074;&#1085;&#1110;&#1095;"
    type "bus"
    population 15000
  ]
  node [
    id 6
    label "&#1055;&#1088;&#1086;&#1084;&#1080;&#1089;&#1083;&#1086;&#1074;&#1072;"
    district "&#1057;&#1093;&#1110;&#1076;"
    type "metro"
    population 45000
  ]
  node [
    id 7
    label "&#1047;&#1072;&#1074;&#1086;&#1076;&#1089;&#1100;&#1082;&#1072;"
    district "&#1057;&#1093;&#1110;&#1076;"
    type "bus"
    population 20000
  ]
  node [
    id 8
    label "&#1053;&#1086;&#1074;&#1072; &#1079;&#1072;&#1073;&#1091;&#1076;&#1086;&#1074;&#1072;"
    district "&#1057;&#1093;&#1110;&#1076;"
    type "bus"
    population 30000
  ]
  node [
    id 9
    label "&#1040;&#1077;&#1088;&#1086;&#1087;&#1086;&#1088;&#1090;"
    district "&#1047;&#1072;&#1093;&#1110;&#1076;"
    type "train"
    population 25000
  ]
  node [
    id 10
    label "&#1058;&#1086;&#1088;&#1075;&#1086;&#1074;&#1080;&#1081; &#1094;&#1077;&#1085;&#1090;&#1088;"
    district "&#1047;&#1072;&#1093;&#1110;&#1076;"
    type "metro"
    population 40000
  ]
  node [
    id 11
    label "&#1057;&#1087;&#1086;&#1088;&#1090;&#1080;&#1074;&#1085;&#1080;&#1081; &#1082;&#1086;&#1084;&#1087;&#1083;&#1077;&#1082;&#1089;"
    district "&#1047;&#1072;&#1093;&#1110;&#1076;"
    type "bus"
    population 20000
  ]
  node [
    id 12
    label "&#1056;&#1110;&#1095;&#1082;&#1086;&#1074;&#1080;&#1081; &#1087;&#1086;&#1088;&#1090;"
    district "&#1055;&#1110;&#1074;&#1076;&#1077;&#1085;&#1100;"
    type "train"
    population 30000
  ]
  node [
    id 13
    label "&#1056;&#1080;&#1085;&#1086;&#1082;"
    district "&#1055;&#1110;&#1074;&#1076;&#1077;&#1085;&#1100;"
    type "bus"
    population 35000
  ]
  node [
    id 14
    label "&#1046;&#1080;&#1090;&#1083;&#1086;&#1074;&#1080;&#1081; &#1084;&#1072;&#1089;&#1080;&#1074;"
    district "&#1055;&#1110;&#1074;&#1076;&#1077;&#1085;&#1100;"
    type "bus"
    population 40000
  ]
  edge [
    source 0
    target 1
    transport_type "metro"
    distance 2.5
    weight 2.5
  ]
  edge [
    source 0
    target 2
    transport_type "metro"
    distance 3.0
    weight 3.0
  ]
  edge [
    source 0
    target 3
    transport_type "metro"
    distance 4.5
    weight 4.5
  ]
  edge [
    source 0
    target 6
    transport_type "metro"
    distance 5.2
    weight 5.2
  ]
  edge [
    source 0
    target 10
    transport_type "metro"
    distance 6.0
    weight 6.0
  ]
  edge [
    source 0
    target 12
    transport_type "bus"
    distance 7.5
    weight 7.5
  ]
  edge [
    source 1
    target 2
    transport_type "bus"
    distance 1.8
    weight 1.8
  ]
  edge [
    source 1
    target 10
    transport_type "bus"
    distance 5.5
    weight 5.5
  ]
  edge [
    source 2
    target 6
    transport_type "bus"
    distance 4.8
    weight 4.8
  ]
  edge [
    source 3
    target 4
    transport_type "bus"
    distance 3.5
    weight 3.5
  ]
  edge [
    source 3
    target 5
    transport_type "train"
    distance 5.0
    weight 5.0
  ]
  edge [
    source 3
    target 9
    transport_type "train"
    distance 12.0
    weight 12.0
  ]
  edge [
    source 4
    target 5
    transport_type "bus"
    distance 2.8
    weight 2.8
  ]
  edge [
    source 4
    target 11
    transport_type "bus"
    distance 8.2
    weight 8.2
  ]
  edge [
    source 6
    target 7
    transport_type "bus"
    distance 2.2
    weight 2.2
  ]
  edge [
    source 6
    target 8
    transport_type "metro"
    distance 4.0
    weight 4.0
  ]
  edge [
    source 7
    target 8
    transport_type "bus"
    distance 3.1
    weight 3.1
  ]
  edge [
    source 7
    target 13
    transport_type "bus"
    distance 6.5
    weight 6.5
  ]
  edge [
    source 8
    target 14
    transport_type "bus"
    distance 5.8
    weight 5.8
  ]
  edge [
    source 9
    target 10
    transport_type "train"
    distance 8.5
    weight 8.5
  ]
  edge [
    source 9
    target 11
    transport_type "bus"
    distance 6.3
    weight 6.3
  ]
  edge [
    source 10
    target 11
    transport_type "bus"
    distance 2.7
    weight 2.7
  ]
  edge [
    source 12
    target 13
    transport_type "bus"
    distance 2.0
    weight 2.0
  ]
  edge [
    source 12
    target 14
    transport_type "train"
    distance 4.2
    weight 4.2
  ]
  edge [
    source 13
    target 14
    transport_type "bus"
    distance 2.5
    weight 2.5
  ]
]
