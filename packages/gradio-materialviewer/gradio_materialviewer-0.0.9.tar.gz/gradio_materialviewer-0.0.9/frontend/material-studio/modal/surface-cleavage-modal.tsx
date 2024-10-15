import { Form, Modal, ModalProps, Row, Col, InputNumber } from 'dptd';
import { DraggableModal } from '@@shared/components/draggle-modal';
import React from 'react';
import { I18N } from '@i18n';
import { useAppContext } from '@context';
import { MaterialCleaveParams } from '../model';

interface SurfaceCleavageModalProps extends ModalProps {
    initialValues?: MaterialCleaveParams;
    onValuesChange?: (values: MaterialCleaveParams) => void;
    onFinish?: (values: MaterialCleaveParams) => void;
    onClose?: () => void;
}

export const defaultCleavageValues = {
    h: 1,
    k: 0,
    l: 0,
    depth: 1,
};

export const SurfaceCleavageModal: React.FC<SurfaceCleavageModalProps> = React.memo(function SurfaceCleavageModal(
    props
) {
    const { initialValues, onValuesChange = () => {}, onFinish = () => {}, onClose = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();
    const [form] = Form.useForm();

    return (
        <DraggableModal
            mask={false}
            {...modalProps}
            title={trans(I18N.material3D.cleaveSurface)}
            onOk={() => {
                const values = form.getFieldsValue();
                onFinish({ ...values });
                (modalProps.onCancel as any)?.();
            }}
            onCancel={() => {
                onClose();
                (modalProps.onCancel as any)?.();
            }}
        >
            <Form
                form={form}
                initialValues={{
                    ...defaultCleavageValues,
                    ...initialValues,
                }}
                onValuesChange={(changed, values) => {
                    onValuesChange(values);
                }}
            >
                <div>{trans(I18N.material3D.millerIndex)}</div>
                <Row>
                    <Col span={8}>
                        <Form.Item name={'h'} label="h">
                            <InputNumber
                                precision={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'k'} label="k">
                            <InputNumber
                                precision={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={8}>
                        <Form.Item name={'l'} label="l">
                            <InputNumber
                                precision={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                </Row>

                <Form.Item name={'depth'} label={<span>{trans(I18N.material3D.thickness)}(Å)</span>}>
                    <InputNumber
                        precision={2}
                        onKeyDown={ev => {
                            ev.stopPropagation();
                        }}
                    />
                </Form.Item>
            </Form>
        </DraggableModal>
    );
});
