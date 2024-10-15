
import gradio as gr
from app import demo as app
import os

_docs = {'MaterialViewer': {'description': 'Creates a very simple textbox for user to enter string input or display string output.', 'members': {'__init__': {'value': {'type': 'typing.Union[str, typing.Callable, NoneType][\n    str, Callable, None\n]', 'default': 'None', 'description': 'default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'placeholder': {'type': 'str | None', 'default': 'None', 'description': 'placeholder hint to provide behind textbox.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'component name in interface.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'rtl': {'type': 'bool', 'default': 'False', 'description': 'If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'materialFile': {'type': 'str | None', 'default': 'None', 'description': None}, 'format': {'type': 'str | None', 'default': 'None', 'description': None}, 'height': {'type': 'int', 'default': '240', 'description': None}, 'style': {'type': 'str | None', 'default': '"BallAndStick"', 'description': None}, 'latticeInfoVisible': {'type': 'bool', 'default': 'False', 'description': None}}, 'postprocess': {'value': {'type': 'str | None', 'description': 'Expects a {str} returned from function and sets textarea value to it.'}}, 'preprocess': {'return': {'type': 'str | None', 'description': 'Passes text value as a {str} into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the MaterialViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the MaterialViewer.'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the MaterialViewer is focused.'}, 'update': {'type': None, 'default': None, 'description': ''}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'MaterialViewer': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_materialviewer`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_materialviewer/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_materialviewer"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_materialviewer
```

## Usage

```python

import gradio as gr
from gradio_materialviewer import MaterialViewer

data1 = \"\"\"# generated using pymatgen
data_Na2CrNiF7
_symmetry_space_group_name_H-M   'P 1'
_cell_length_a   7.27889000
_cell_length_b   7.33433943
_cell_length_c   7.33434858
_cell_angle_alpha   89.52670711
_cell_angle_beta   60.24975983
_cell_angle_gamma   60.24971896
_symmetry_Int_Tables_number   1
_chemical_formula_structural   Na2CrNiF7
_chemical_formula_sum   'Na4 Cr2 Ni2 F14'
_cell_volume   280.04214068
_cell_formula_units_Z   2
loop_
 _symmetry_equiv_pos_site_id
 _symmetry_equiv_pos_as_xyz
  1  'x, y, z'
loop_
 _atom_site_type_symbol
 _atom_site_label
 _atom_site_symmetry_multiplicity
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
  Cr  Cr1  1  0.50000000  0.50000000  0.50000000  1.0
  Cr  Cr2  1  0.50000000  0.00000000  1.00000000  1.0
  F  F1  1  0.84896000  0.40104000  0.90104000  1.0
  F  F2  1  0.15104000  0.59896000  0.09896000  1.0
  F  F5  1  0.26844000  0.14265000  0.32047000  1.0
  F  F6  1  0.73156000  0.85735000  0.67953000  1.0
  F  F7  1  0.73156000  0.17953000  0.35735000  1.0
  F  F8  1  0.26844000  0.82047000  0.64265000  1.0
  F  F13  1  0.75447000  0.82680000  0.05766000  1.0
  F  F14  1  0.63893000  0.17320000  0.94234000  1.0
  F  F15  1  0.63893000  0.44234000  0.67320000  1.0
  F  F16  1  0.75447000  0.55766000  0.32680000  1.0
  F  F17  1  0.24553000  0.17320000  0.94234000  1.0
  F  F18  1  0.36107000  0.82680000  0.05766000  1.0
  F  F19  1  0.36107000  0.55766000  0.32680000  1.0
  F  F20  1  0.24553000  0.44234000  0.67320000  1.0
  Na  Na1  1  0.00000000  0.00000000  0.00000000  1.0
  Na  Na2  1  0.00000000  0.50000000  0.50000000  1.0
  Na  Na5  1  0.50000000  1.00000000  0.50000000  1.0
  Na  Na6  1  1.00000000  0.00000000  0.50000000  1.0
  Ni  Ni1  1  0.00000000  0.50000000  0.00000000  1.0
  Ni  Ni2  1  0.50000000  0.50000000  0.00000000  1.0
\"\"\"
data2 = \"\"\"Si72 Ti24 Mo12 \n1.0\n1.3846361559434408e+01 0.0000000000000000e+00 0.0000000000000000e+00 \n4.5603121815906080e+00 7.8801080312678193e+00 0.0000000000000000e+00 \n-2.6863950750812565e-01 -5.1717325524110236e-02 1.3016015481941894e+01 \nSi Ti Mo \n72 24 12 \nCartesian\n  12.5943083987    3.2619731187    3.1433537355\n  12.4599886450    3.2361144560    9.6513614765\n  14.8744644895    7.2020271344    3.1433537355\n  14.7401447358    7.1761684716    9.6513614765\n  13.7885083993    1.0176631177    1.0101637345\n  13.6541886455    0.9918044550    7.5181714755\n  16.0686644901    4.9577171334    1.0101637345\n  15.9343447363    4.9318584706    7.5181714755\n  10.2350083977    0.6128481176    5.3484937365\n  10.1006886440    0.5869894548   11.8565014774\n  12.5151644885    4.5529021332    5.3484937365\n  12.3808447347    4.5270434704   11.8565014774\n  12.6837083988    0.7103611176    3.1895037355\n  12.5493886450    0.6845024549    9.6975114765\n  14.9638644896    4.6504151332    3.1895037355\n  14.8295447358    4.6245564705    9.6975114765\n  11.4253083982    2.5099231184    1.1436237346\n  11.2909886445    2.4840644556    7.6516314756\n  13.7054644890    6.4499771340    1.1436237346\n  13.5711447353    6.4241184713    7.6516314756\n  10.2737083977    3.2181731187    5.5640237365\n  10.1393886440    3.1923144560   12.0720314775\n  12.5538644885    7.1582271344    5.5640237365\n  12.4195447348    7.1323684716   12.0720314775\n   7.9153683967    3.2130631187    3.2727137355\n   7.7810486429    3.1872044560    9.7807214765\n  10.1955244875    7.1531171343    3.2727137355\n  10.0612047337    7.1272584716    9.7807214765\n   9.0994983972    1.2789531179    1.1079237346\n   8.9651786435    1.2530944551    7.6159314756\n  11.3796544880    5.2190071335    1.1079237346\n  11.2453347342    5.1931484707    7.6159314756\n  14.8766083998    3.3290531188    5.2777937364\n  14.7422886460    3.3031944560   11.7858014774\n  17.1567644905    7.2691071344    5.2777937364\n  17.0224447368    7.2432484716   11.7858014774\n   5.5597983956    0.6823141176    5.4365837365\n   5.4254786419    0.6564554548   11.9445914775\n   7.8399544864    4.6223681332    5.4365837365\n   7.7056347327    4.5965094705   11.9445914775\n   6.7954283962    2.6319331185    1.0704537346\n   6.6611086424    2.6060744557    7.5784614755\n   9.0755844870    6.5719871341    1.0704537346\n   8.9412647332    6.5461284713    7.5784614755\n   5.6441283957    3.3173131188    5.4848537365\n   5.5098086419    3.2914544560   11.9928614775\n   7.9242844865    7.2573671344    5.4848537365\n   7.7899647327    7.2315084716   11.9928614775\n   3.2339783946    3.4125931188    3.3120337356\n   3.0996586409    3.3867344560    9.8200414765\n   5.5141344854    7.3526471344    3.3120337356\n   5.3798147317    7.3267884717    9.8200414765\n   4.5115083952    1.3772631179    1.0095537345\n   4.3771886414    1.3514044551    7.5175614755\n   6.7916644860    5.3173171335    1.0095537345\n   6.6573447322    5.2914584708    7.5175614755\n   1.0728783937    0.7667711176    5.4178737365\n   0.9385586399    0.7409124549   11.9258814775\n   3.3530344845    4.7068251333    5.4178737365\n   3.2187147307    4.6809664705   11.9258814775\n   3.5918083948    0.5796661176    3.3862237356\n   3.4574886410    0.5538074548    9.8942314766\n   5.8719644856    4.5197201332    3.3862237356\n   5.7376447318    4.4938614704    9.8942314766\n   2.2437283942    2.5873231184    1.1980437346\n   2.1094086404    2.5614644557    7.7060514756\n   4.5238844850    6.5273771341    1.1980437346\n   4.3895647312    6.5015184713    7.7060514756\n   8.1333883968    0.6340201176    3.2715337355\n   7.9990686430    0.6081614548    9.7795414765\n  10.4135444876    4.5740741332    3.2715337355\n  10.2792247338    4.5482154705    9.7795414765\n   7.9900183967    1.8571331181    5.3069737364\n   7.8556986430    1.8312744554   11.8149814774\n  10.2701744875    5.7971871338    5.3069737364\n  10.1358547338    5.7713284710   11.8149814774\n   5.7294483957    1.9965931182    3.2089237355\n   5.5951286420    1.9707344554    9.7169314765\n   8.0096044865    5.9366471338    3.2089237355\n   7.8752847328    5.9107884711    9.7169314765\n  10.2786083977    1.9322231182    3.1895437355\n  10.1442886440    1.9063644554    9.6975514765\n  12.5587644885    5.8722771338    3.1895437355\n  12.4244447348    5.8464184710    9.6975514765\n  12.6003083987    1.9652531182    5.4992937365\n  12.4659886450    1.9393944554   12.0073014775\n  14.8804644895    5.9053071338    5.4992937365\n  14.7461447358    5.8794484710   12.0073014775\n   3.3319683947    2.0216131182    5.3626437365\n   3.1976486409    1.9957544554   11.8706514774\n   5.6121244855    5.9616671338    5.3626437365\n   5.4778047317    5.9358084711   11.8706514774\n  14.8864083998    1.9509331182    3.3404537356\n  14.7520886460    1.9250744554    9.8484614765\n  17.1665644905    5.8909871338    3.3404537356\n  17.0322447368    5.8651284710    9.8484614765\n  13.9479083993    3.8710931190    1.0219437345\n  13.8135886456    3.8452344562    7.5299514755\n  16.2280644901    7.8111471346    1.0219437345\n  16.0937447364    7.7852884719    7.5299514755\n   6.8342583962    0.0615311173    1.0295137346\n   6.6999386425    0.0356724546    7.5375214755\n   9.1144144870    4.0015851330    1.0295137346\n   8.9800947333    3.9757264702    7.5375214755\n   2.2482383942    0.0163334173    1.2432337346\n   2.1139186404   -0.0095252455    7.7512414756\n   4.5283944850    3.9563874329    1.2432337346\n   4.3940747312    3.9305287702    7.7512414756\n\"\"\"

with gr.Blocks() as demo:
    with gr.Row():
        test = MaterialViewer(materialFile=data1, format='cif', height=480)
    with gr.Row():
        update_button = gr.Button("Update")

    def updateFile():
        return MaterialViewer(materialFile=data2, format='POSCAR', height=360)
    
    update_button.click(
        updateFile,
        outputs=[test],
    )

if __name__ == "__main__":
    demo.launch()
```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `MaterialViewer`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["MaterialViewer"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["MaterialViewer"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes text value as a {str} into the function.
- **As output:** Should return, expects a {str} returned from function and sets textarea value to it.

 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "MaterialViewer-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          MaterialViewer: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
