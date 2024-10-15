from __future__ import annotations

from typing import Any, Callable

from gradio.components.base import FormComponent
from gradio.events import Events
from ase import Atoms, Atom
from ase.io import read, write
from ase.spacegroup import get_spacegroup
import io
import json
import numpy as np
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class MaterialViewer(FormComponent):
    """
    Creates a very simple textbox for user to enter string input or display string output.
    """

    EVENTS = [
        Events.change,
        Events.input,
        Events.submit,
        'update',
    ]

    # def get_info(self, file, format='POSCAR'):
    #     # 创建一个 StringIO 对象
    #     file_obj = io.StringIO()
    #     # 向文件对象中写入数据
    #     file_obj.write(file)
    #     # 将文件对象的指针移动到文件开始位置
    #     file_obj.seek(0)
    #     ase_format = self.format_to_ase(format)
    #     for structure in read(file_obj, index=":", format=ase_format):
    #         formulas = structure.get_chemical_symbols()
    #         cartesian_coords = structure.get_positions()
    #         if structure.pbc.all():
    #             lattice = structure.cell
    #             matrix = lattice.array
    #             length = lattice.lengths()
    #             angle = lattice.angles()
    #             spacegroup = [get_spacegroup(structure).no, get_spacegroup(structure).symbol]
    #             fractional_coords = structure.get_scaled_positions()
    #             atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart, "frac_coord": frac} for
    #                     index, (formula, cart, frac) in enumerate(zip(formulas, cartesian_coords, fractional_coords))]
    #             results = {"atoms": atoms, "matrix": matrix, "length": length, "angle": angle, "spacegroup": spacegroup}
    #         else:
    #             atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart} for
    #                     index, (formula, cart) in enumerate(zip(formulas, cartesian_coords))]
    #             results = {"atoms": atoms}
    #     return results

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        placeholder: str | None = None,
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        rtl: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        materialFile: str | None = None,
        format: str | None = None,
        height: int = 240,
        style: str | None = 'BallAndStick',
        latticeInfoVisible: bool = False
    ):
        """
        Parameters:
            value: default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.
            placeholder: placeholder hint to provide behind textbox.
            label: component name in interface.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            rtl: If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
        """
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, dict):
                return {k: convert_numpy(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_numpy(v) for v in obj]
            return obj

        def format_to_ase(format):
            if format == 'POSCAR':
                ase_format = 'vasp'
            elif format == 'dump':
                ase_format = 'lammps-dump-text'
            else:
                ase_format = format
            return ase_format

        def get_info(file, format='POSCAR'):
            # 创建一个 StringIO 对象
            file_obj = io.StringIO()
            # 向文件对象中写入数据
            file_obj.write(file)
            # 将文件对象的指针移动到文件开始位置
            file_obj.seek(0)
            def structure_generator():
                ase_format = format_to_ase(format)
                for structure in read(file_obj, index=":", format=ase_format):
                    formulas = structure.get_chemical_symbols()
                    cartesian_coords = structure.get_positions()
                    if structure.pbc.all():
                        lattice = structure.cell
                        matrix = lattice.array
                        length = lattice.lengths()
                        angle = lattice.angles()
                        spacegroup = [get_spacegroup(structure).no, get_spacegroup(structure).symbol]
                        fractional_coords = structure.get_scaled_positions()
                        atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart, "frac_coord": frac} for
                                index, (formula, cart, frac) in enumerate(zip(formulas, cartesian_coords, fractional_coords))]
                        results = {"atoms": atoms, "matrix": matrix, "length": length, "angle": angle, "spacegroup": spacegroup}
                    else:
                        atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart} for
                                index, (formula, cart) in enumerate(zip(formulas, cartesian_coords))]
                        results = {"atoms": atoms}
                    yield results
            yield from structure_generator()
        materialFile = json.dumps(convert_numpy(list(get_info(materialFile, format))))
        self.materialFile = materialFile
        self.format = format
        self.height = height
        self.style = style
        self.latticeInfoVisible = latticeInfoVisible
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
        )


    # def convert_numpy(self, obj):
    #     if isinstance(obj, np.ndarray):
    #         return obj.tolist()
    #     if isinstance(obj, dict):
    #         return {k: self.convert_numpy(v) for k, v in obj.items()}
    #     if isinstance(obj, list):
    #         return [self.convert_numpy(v) for v in obj]
    #     return obj

    # def format_to_ase(self, format):
    #     if format == 'POSCAR':
    #         ase_format = 'vasp'
    #     elif format == 'dump':
    #         ase_format = 'lammps-dump-text'
    #     else:
    #         ase_format = format
    #     return ase_format

    # def get_info(self, file, format='POSCAR'):
    #     # 创建一个 StringIO 对象
    #     file_obj = io.StringIO()
    #     # 向文件对象中写入数据
    #     file_obj.write(file)
    #     # 将文件对象的指针移动到文件开始位置
    #     file_obj.seek(0)
    #     def structure_generator():
    #         ase_format = self.format_to_ase(format)
    #         for structure in read(file_obj, index=":", format=ase_format):
    #             formulas = structure.get_chemical_symbols()
    #             cartesian_coords = structure.get_positions()
    #             if structure.pbc.all():
    #                 lattice = structure.cell
    #                 matrix = lattice.array
    #                 length = lattice.lengths()
    #                 angle = lattice.angles()
    #                 spacegroup = [get_spacegroup(structure).no, get_spacegroup(structure).symbol]
    #                 fractional_coords = structure.get_scaled_positions()
    #                 atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart, "frac_coord": frac} for
    #                         index, (formula, cart, frac) in enumerate(zip(formulas, cartesian_coords, fractional_coords))]
    #                 results = {"atoms": atoms, "matrix": matrix, "length": length, "angle": angle, "spacegroup": spacegroup}
    #             else:
    #                 atoms = [{"id": index + 1, "formula": formula, "cart_coord": cart} for
    #                         index, (formula, cart) in enumerate(zip(formulas, cartesian_coords))]
    #                 results = {"atoms": atoms}
    #             yield results
    #     yield from structure_generator()

    def preprocess(self, payload: str | None) -> str | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        return None if payload is None else str(payload)

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {str} returned from function and sets textarea value to it.
        Returns:
            The value to display in the textarea.
        """
        return None if value is None else str(value)

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "Hello!!"

    def example_value(self) -> Any:
        return "Hello!!"    

    # def update(self, materialFile: str, format: str) -> any:
    #     self.materialFile = json.dumps(self.convert_numpy(list(self.get_info(materialFile, format))))
    #     res = {}
    #     res['materialFile'] = self.materialFile
    #     print('Update')
    #     return res
