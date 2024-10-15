import { Form, Modal, ModalProps, Row, Select, Col, InputNumber } from 'dptd';
import { DraggableModal } from '@@shared/components/draggle-modal';
import React, { useEffect, useMemo, useState } from 'react';
import { I18N } from '@i18n';
import { useAppContext } from '@context';
import { getSpaceGroupByNo, useSpaceGroup } from '../hooks/useSpaceGroup';
import { LatticeParams } from '../model';

interface LatticeModalProps extends ModalProps {
    lattice?: LatticeParams;
    onFinish?: (lattice: LatticeParams) => void;
}

export const LatticeModalStatus = {
    open: false,
};

export const LatticeModal: React.FC<LatticeModalProps> = React.memo(function LatticeModal(props) {
    const { lattice, onFinish = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();
    const { crystalSystem, spaceGroupOptions, setCrystalSystemByNo } = useSpaceGroup(lattice?.spacegroup.no);
    const [spaceGroupNo, setSpaceGroupNo] = useState(lattice?.spacegroup.no || 1);
    const [form] = Form.useForm();

    const initialValues = useMemo(() => {
        const defaultValues = {
            a: 10,
            b: 10,
            c: 10,
            alpha: 90,
            beta: 90,
            gamma: 90,
        };
        const values = { ...defaultValues, ...lattice, ...crystalSystem.initialValues };
        return crystalSystem.convert(values);
    }, []);

    useEffect(() => {
        LatticeModalStatus.open = true;

        return () => {
            LatticeModalStatus.open = false;
        };
    }, []);

    return (
        <DraggableModal
            mask={false}
            {...modalProps}
            // title={trans(I18N.material3D.addVacuumLayer)}
            title={trans(I18N.material3D.buildLattice)}
            onOk={() => {
                const values = form.getFieldsValue();
                const spacegroup = getSpaceGroupByNo(spaceGroupNo);
                onFinish({ ...values, spacegroup });
                (modalProps.onCancel as any)?.();
            }}
        >
            <Form
                form={form}
                initialValues={initialValues}
                onValuesChange={(changed, values) => {
                    form.setFieldsValue(crystalSystem.convert(values));
                }}
            >
                <Form.Item label={trans(I18N.material3D.spaceGroup)}>
                    <Select
                        disabled
                        options={spaceGroupOptions}
                        value={spaceGroupNo}
                        onChange={no => {
                            setSpaceGroupNo(no);
                            const system = setCrystalSystemByNo(no);
                            const values = form.getFieldsValue();
                            form.setFieldsValue(system.convert(values));
                        }}
                    />
                </Form.Item>
                <Row>
                    <Col span={8}>
                        <Form.Item name={'a'} label="a">
                            <InputNumber
                                disabled={crystalSystem.disabled.a}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'b'} label="b">
                            <InputNumber
                                disabled={crystalSystem.disabled.b}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'c'} label="c">
                            <InputNumber
                                disabled={crystalSystem.disabled.c}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={8}>
                        <Form.Item name={'alpha'} label="α">
                            <InputNumber
                                disabled={crystalSystem.disabled.alpha}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'beta'} label="β">
                            <InputNumber
                                disabled={crystalSystem.disabled.beta}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'gamma'} label="γ">
                            <InputNumber
                                disabled={crystalSystem.disabled.gamma}
                                precision={3}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
            {/* <div>{crystalSystem.description}</div> */}
        </DraggableModal>
    );
});
