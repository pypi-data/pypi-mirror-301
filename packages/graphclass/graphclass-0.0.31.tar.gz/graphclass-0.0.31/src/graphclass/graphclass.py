"""
Drawing Module

This module provides a class, Drawing, for generating diagrams with nodes and relationships
  using the Graphviz engine. It simplifies the process of creating graphical representations
  of objects, their hierarchy, and relationships.

Class:
- `Drawing`: Manages the creation and rendering of diagrams.

Methods:
- `add_item(node_id, node=None, cluster=None, point=None)`:
      Add an item to the diagram with the specified attributes.
- `add_parent(node_id, parent)`: Add a parent-child relationship between items.
- `add_list(node_id, lst)`: Represent a list of items associated with an object in the diagram.
- `add_link(node_id, link, label="")`: Add a link between two items with an optional label.

Usage:
- ...

Author: Pavel ERESKO
"""



from graphviz import Digraph, Source

from jinja2 import Template

import importlib.resources

def insert_line_breaks(text, interval = 40):
    lines = text.split('\n')
    result = []

    for line in lines:
        words = line.split()
        current_line = ""
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 > interval and len(result) > 0:
                result.append(current_line)
                current_line = word
                current_length = len(word)
            else:
                if current_line:
                    current_line += " "
                current_line += word
                current_length += len(word) + 1

        result.append(current_line)
        result.append("")

    if result and result[-1] == "":
        result.pop()

    return "<br/>".join(result)

def simple_node_label(text):
    ''' html code for cluster header '''
    return f'''<
        <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
            <TR>
                <TD><B>{text}</B></TD>
            </TR>
        </TABLE>
    >'''

def simple_list_label(listname, listitems):
    label = f'<TR><TD BGCOLOR="#A9DFBF"><B>{listname}</B></TD></TR>\n'
    for listitem in listitems:
        label += f'<TR><TD BGCOLOR="white" PORT="{listitem}"><FONT POINT-SIZE="12.0">{listitem}</FONT></TD></TR>\n'

    label = f'''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        {label}
        </TABLE>
    >'''

    return label

def node_label(obj, DRAW):
    ''' html code for node '''
    draw  = type(obj).Draw
    color = type(obj).Color

    res = ""
    if draw & DRAW.VIEW:
        val = obj.get_view()
        if val:
            res = res + f'''
                <TR>
                    <TD {obj.get_href()} BGCOLOR="{color}" PORT="p0"><B>{insert_line_breaks(val)}</B></TD>
                </TR>
            '''
    if draw & DRAW.EXT:
        val = obj.get_ext()
        if val:
            res = res + f'''
                <TR>
                    <TD BGCOLOR="white" PORT="p1"><FONT POINT-SIZE="12.0">{insert_line_breaks(val)}</FONT></TD>
                </TR>
            '''
    if draw & DRAW.ICON:
        val = obj.get_icon()
        if val:
            res = res + f'''
                <TR>
                    <TD BGCOLOR="white" PORT="p2"><IMG SRC="{val}"/></TD>
                </TR>
            '''
    if draw & DRAW.CLASS:
        val = obj.get_class_view()
        if val:
            res = res + f'''
                <TR>
                    <TD BGCOLOR="white" PORT="p4"><FONT POINT-SIZE="8.0">{val}</FONT></TD>
                </TR>
            '''
    if draw & DRAW.ID:
        val = obj.get_id()
        if val:
            res = res + f'''
                <TR>
                    <TD BGCOLOR="{color}" PORT="p3"><FONT POINT-SIZE="8.0">{val}</FONT></TD>
                </TR>
            '''
        
    if res == "":
        val = obj.get_id()
        res = res + f'''
            <TR>
                <TD BGCOLOR="{color}" PORT="p0"><B>{val}</B></TD>
            </TR>
        '''

    return f'''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        {res}
        </TABLE>
    >'''

def cluster_label(obj, DRAW):
    ''' html code for cluster header '''
    draw = obj.Draw

    res0 = ""

    val = obj.get_icon()
    if val:
        if draw & DRAW.ICON:
            res0 = res0 + f'''
                <TD ROWSPAN="3"><IMG SRC="{val}"/></TD>
            '''

    val = obj.get_view()
    if val:
        if draw & DRAW.VIEW:
            res0 = res0 + f'''
                <TD {obj.get_href()}><B>{insert_line_breaks(val)}</B></TD>
            '''

    if res0 != "":
        res0 = f'''
        <TR>
            {res0}
        </TR>
        '''

    res1 = ""

    if draw & DRAW.EXT:
        val = obj.get_ext()
        if val:
            res1 = res1 + f'''
            <TR>
                <TD BGCOLOR="white"><FONT POINT-SIZE="12.0">{insert_line_breaks(val)}</FONT></TD>
            </TR>
            '''

    val = obj.get_class_view()
    if val:
        if draw & DRAW.CLASS:
            res1 = res1 + f'''
                <TR>
                    <TD><FONT POINT-SIZE="8.0">{val}</FONT></TD>
                </TR>
                '''

    val = obj.get_id()
    if val:
        if draw & DRAW.ID:
            res1 = res1 + f'''
            <TR>
                <TD><FONT POINT-SIZE="8.0">{val}</FONT></TD>
            </TR>
            '''

    if res0 == "" and res1 == "":
        val = obj.get_id()
        res0 = res0 + f'''
        <TR>
            <TD PORT="p0"><B>{val}</B></TD>
        </TR>
    '''

    return f'''<
        <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
            {res0}
            {res1}
        </TABLE>
    >'''

def list_label(list_view, listitems):
    label = f'<TR><TD BGCOLOR="#A9DFBF"><B><FONT POINT-SIZE="9.0">{list_view}</FONT></B></TD></TR>\n'
    draw_it = False
    for list_item in listitems:
        if list_item is None:
            continue
        draw_it = True
        label += f'<TR><TD {list_item["href"]} BGCOLOR="white" PORT="{list_item["id"]}"><FONT POINT-SIZE="9.0">{insert_line_breaks(list_item["view"])}</FONT></TD></TR>\n'

    if not draw_it:
        return

    label = f'''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
        {label}
        </TABLE>
    >'''

    return label

def get_resource_path(path, file):
    with importlib.resources.path(path, file) as res_path:
        return str(res_path)


class Drawing:
    ''' Class that provide drawing structure of nodes with parent, list, and links relations '''
    def __init__(self):
        self.items   = {}
        self.parents = {}
        self.lists   = {}
        self.links   = []

        self.linked = None

    def item_view(self,
        label = "[Item]", shape = "plaintext", style = 'filled', fillcolor = None, width = 0.1
    ):
        ''' Parameter passing function '''
        return {
            "label": label, "shape": shape, "style": style, "fillcolor": fillcolor, "width": width,
        }

    def add_item(self, node_id, node = None, cluster = None, point = None):
        ''' Add node with html representation '''
        if not node_id in self.items:
            self.items[node_id] = {}

        for name, par in {"node" : node, "cluster" : cluster, "point" : point}.items():
            if par is None:
                continue

            labeldict = par
            if name == "node" and isinstance(par, str):
                labeldict = self.item_view(par)

            self.items[node_id][name] = labeldict

    def add_parent(self, node_id, parent):
        ''' Add parent relation '''
        self.parents[node_id] = parent

    def add_list(self, node_id, node_list):
        ''' Add list relation '''
        self.lists[node_id] = node_list

    def add_link(self, node_id, link, label = ""):
        ''' Add link relation '''
        self.links.append((node_id, link, label))

    def print(self):
        ''' Print nodes and relations added '''
        print("\nDrawing")

        print("\tItems  :")
        for i, data in self.items  .items():
            print(i, end=' ')
        print()

        print("\tParents:")
        for i, data in self.parents.items():
            print(f"{i} -> {data}")

        print("\tLists  :")
        for i, data in self.lists  .items():
            print(i)

        print("\tLinks  :")
        for node_id, link, label in self.links:
            print(f"{node_id} --[{label}]--> {link}")

    def draw_rec(self, parent, grand_digraph):
        ''' Recursively draws the nodes '''
        items = [node_id for node_id in self.items if not node_id in
                    [chi for chi, par in self.parents.items() if par in self.items]
                ] if parent is None \
                  else [node_id for node_id, par in self.parents.items() if par == parent]

        if len(items) == 0:
            view = self.items[parent]["node"]
            grand_digraph.node(name=parent, shape=view["shape"], label = view["label"])

        else:
            par_context = None
            par_digraph = None if parent is not None else grand_digraph

            for node_id in items:
                if par_digraph is None:
                    par_context = grand_digraph.subgraph(name = "cluster_" + parent)
                    par_digraph = par_context.__enter__()

                    view = self.items[parent]["cluster"]

                    # label = f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
                    #             {view["label"]}
                    #             </TABLE>>'''
                    label = view["label"]
                    # print(label.replace("\n", ""))

                    par_digraph.attr(
                        label = label,
                        style = view["style"],
                        fillcolor = view["fillcolor"]
                    )

                    if parent in self.linked:
                        view = self.items[parent]["point"]
                        par_digraph.node(name=parent, shape=view["shape"], width=view["width"])

                self.draw_rec(node_id, par_digraph)

            if par_context is not None:
                par_context.__exit__(None, None, None)

    def dot(self, name):
        ''' Draws the structure of nodes with all the relations '''
        dot = Digraph(name)

        self.linked = {}
        for node_id, link, label in self.links:
            self.linked[node_id] = True
            self.linked[link] = True
            dot.edge(node_id, link, label = label)

        if len(self.items) > 0:
            self.draw_rec(None, dot)

        self.linked = None

        return dot
    
    def source(self, name):
        return self.dot(name).source

    def svg(self, name, engine = "dot"):
# engine:
# dot (default) - используется для иерархической (directed) визуализации графов, лучше всего подходит
#  для направленных графов. Движок строит граф по уровням, что делает его удобным для отображения деревьев
#  и других структур с иерархией.
# neato - использует алгоритм силового направления для расположения графа, подходящий для неориентированных графов.
# fdp - также использует метод силового направления, но с другим подходом, более подходящий для плотных графов.
# sfdp - оптимизированная версия fdp для масштабных графов.
# twopi - рисует графы в радиальной раскладке. Удобен для графов, где один узел может быть центром,
#  а остальные узлы расположены вокруг него по окружности.
# circo - рисует графы с циркулярной раскладкой. Подходит для круговых графов и рёбер с кольцевыми структурами.
# osage - предназначен для мультиграфов, где есть несколько рёбер между одними и теми же парами узлов.
# patchwork - строит графы в виде вложенных прямоугольников, подходит для работы с деревьями.

        dot = self.dot(name)
        dot.engine = engine

        try:
            svg_str = dot.pipe(format='svg').decode('utf-8')
        except Exception as e:
            print(f"Draw error: {str(e)}")
            return ""

        svg_str = '\n'.join(svg_str.split('\n')[3:])

        return svg_str

    def html(self, name, engine = "dot", reload_time=0):
        svg_str = self.svg(name, engine)

        path = get_resource_path('graphclass.template', 'html.j2')
        with open(path, 'r') as file:
            template_str = file.read()
        template = Template(template_str)

        output = template.render(content=svg_str, name=name, reload_time=reload_time)
        return output

    def png(self, name, png_path, engine = "dot"):
        svg_content = self.svg(name, engine)
        graph = Source(svg_content, format='png')
        graph.render(filename=png_path, cleanup=True)
