import { ModalProps, InputNumber, Button } from 'dptd';
import { DraggableModal } from '@@shared/components/draggle-modal';
import React, { useState } from 'react';
import { I18N } from '@i18n';
import { clsx } from 'clsx';
import BrmIcon from '@@icons';
import { useAppContext } from '@context';
import { useSubjectState } from '@@shared/hooks/useSubjectState';
import { BehaviorSubject } from 'rxjs';
import { Atom } from '../model';

import styles from './rotate-atom-modal.module.less';

interface RotateAtomModalProps extends ModalProps {
    selectedAtomsSubject: BehaviorSubject<Atom[]>;
    onStep?: (angle: number[]) => void;
}

export const RotateAtomModal: React.FC<RotateAtomModalProps> = React.memo(function RotateAtomModal(props) {
    const { selectedAtomsSubject, onStep = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();

    const selectedAtoms = useSubjectState(selectedAtomsSubject);
    const [angle, setAngle] = useState(45);

    return (
        <DraggableModal mask={false} {...modalProps} width={380} title={trans(I18N.material3D.rotate)} footer={null}>
            <div className={styles.box}>
                <div className={styles['box-left']}>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.up)}
                        onClick={() => {
                            onStep([-angle, 0, 0]);
                        }}
                    >
                        <BrmIcon name="rotate-y-negative" />
                    </Button>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.down)}
                        onClick={() => {
                            onStep([angle, 0, 0]);
                        }}
                    >
                        <BrmIcon name="rotate-y-positive" />
                    </Button>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.left)}
                        onClick={() => {
                            onStep([0, -angle, 0]);
                        }}
                    >
                        <BrmIcon name="rotate-x-negative" />
                    </Button>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.right)}
                        onClick={() => {
                            onStep([0, angle, 0]);
                        }}
                    >
                        <BrmIcon name="rotate-x-positive" />
                    </Button>
                </div>
                <div className={styles['box-right']}>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.up)}
                        onClick={() => {
                            onStep([0, 0, angle]);
                        }}
                    >
                        <BrmIcon name="rotate-z-positive" />
                    </Button>
                    <Button
                        type="text"
                        disabled={!selectedAtoms?.length}
                        className={clsx(styles.btn, styles.down)}
                        onClick={() => {
                            onStep([0, 0, -angle]);
                        }}
                    >
                        <BrmIcon name="rotate-z-negative" />
                    </Button>
                </div>
            </div>
            <div className="flex items-center mt-20">
                <span
                    className="mr-8 text-h6"
                    style={{
                        flexShrink: 0,
                    }}
                >
                    {trans(I18N.material3D.angle)}
                </span>
                <InputNumber
                    className={styles.input}
                    value={angle}
                    onChange={v => setAngle(v ? v % 360 : 0)}
                    precision={2}
                    step={1}
                    min={0.1}
                    onKeyDown={ev => {
                        ev.stopPropagation();
                    }}
                />
            </div>
        </DraggableModal>
    );
});
