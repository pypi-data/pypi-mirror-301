import { Form, ModalProps, Row, Col, InputNumber } from 'dptd';
import { DraggableModal } from '@@shared/components/draggle-modal';
import React from 'react';
import { I18N } from '@i18n';
import { useAppContext } from '@context';

interface AddVacuumLayerModalProps extends ModalProps {
    onFinish?: (values: { c: number }) => void;
}

export const AddVacuumLayerModal: React.FC<AddVacuumLayerModalProps> = React.memo(function AddVacuumLayerModal(props) {
    const { onFinish = () => {}, ...modalProps } = props;
    const [form] = Form.useForm();
    const { trans } = useAppContext();

    return (
        <DraggableModal
            mask={false}
            {...modalProps}
            title={trans(I18N.material3D.vacuumLayerThickness)}
            onOk={() => {
                const values = form.getFieldsValue();
                onFinish({ ...values });
                (modalProps.onCancel as any)?.();
            }}
        >
            <Form
                form={form}
                initialValues={{
                    c: 1,
                }}
            >
                <Row>
                    <Col span={8}>
                        <Form.Item name={'c'} label={<span>{trans(I18N.material3D.thickness)}(Å)</span>}>
                            <InputNumber
                                precision={0}
                                onKeyDown={ev => {
                                    ev.stopPropagation();
                                }}
                            />
                        </Form.Item>
                    </Col>
                </Row>
            </Form>
        </DraggableModal>
    );
});
