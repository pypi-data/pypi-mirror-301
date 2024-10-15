import { Form, Modal, ModalProps, Select } from 'dptd';
// import { DraggableModal } from '@@shared/components/draggle-modal';
import React from 'react';
import { I18N } from '@i18n';
import { useAppContext } from '@context';
import { RepresentationType } from 'dpmol';

interface SettingModalProps extends ModalProps {
    initialValues?: { reprType: RepresentationType };
    onFinish?: (values: { reprType: RepresentationType }) => void;
}

export const SettingModal: React.FC<SettingModalProps> = React.memo(function SettingModal(props) {
    const { initialValues, onFinish = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();
    const [form] = Form.useForm();

    return (
        <Modal
            // mask={false}
            {...modalProps}
            title={trans(I18N.material3D.setting)}
            onOk={() => {
                const values = form.getFieldsValue();
                onFinish({ ...values });
                (modalProps.onCancel as any)?.();
            }}
        >
            <Form form={form} initialValues={initialValues}>
                <Form.Item name={'reprType'} label={trans(I18N.material3D.style)}>
                    <Select
                        options={[
                            {
                                label: trans(I18N.material3D.ballAndStick),
                                value: RepresentationType.BallAndStick,
                            },
                            {
                                label: trans(I18N.material3D.stick),
                                value: RepresentationType.Stick,
                            },
                            {
                                label: trans(I18N.material3D.line),
                                value: RepresentationType.Line,
                            },
                            {
                                label: trans(I18N.material3D.cpk),
                                value: RepresentationType.CPK,
                            },
                        ]}
                    />
                </Form.Item>
            </Form>
        </Modal>
    );
});
