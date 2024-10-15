import { Form, Modal, ModalProps, Row, Col, InputNumber } from 'dptd';
import { DraggableModal } from '@@shared/components/draggle-modal';
import { I18N } from '@i18n';
import { useAppContext } from '@context';
import React from 'react';

interface AbcModalProps extends ModalProps {
    xyz: number[];
    onFinish?: (xyz: number[]) => void;
}

export const AbcModal: React.FC<AbcModalProps> = React.memo(function AbcModal(props) {
    const { xyz, onFinish = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();
    const [form] = Form.useForm();

    return (
        <Modal
            // mask={false}
            {...modalProps}
            title={trans(I18N.material3D.fractionalCoord)}
            onOk={() => {
                const values = form.getFieldsValue();
                const xyz = [values.x, values.y, values.z] as number[];
                onFinish(xyz);
                (modalProps.onCancel as any)?.();
            }}
        >
            <Form
                form={form}
                initialValues={{
                    x: xyz[0],
                    y: xyz[1],
                    z: xyz[2],
                }}
            >
                <Row>
                    <Col span={8}>
                        <Form.Item name={'x'} label="x">
                            <InputNumber
                                precision={3}
                                max={1}
                                min={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'y'} label="y">
                            <InputNumber
                                precision={3}
                                max={1}
                                min={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'z'} label="z">
                            <InputNumber
                                precision={3}
                                max={1}
                                min={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </Modal>
    );
});
