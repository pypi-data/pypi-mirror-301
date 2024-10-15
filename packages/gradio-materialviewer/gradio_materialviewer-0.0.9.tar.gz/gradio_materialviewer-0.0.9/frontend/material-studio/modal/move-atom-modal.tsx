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

import styles from './move-atom-modal.module.less';

interface MoveAtomModalProps extends ModalProps {
    selectedAtomsSubject: BehaviorSubject<Atom[]>;
    onStep?: (length: number[]) => void;
}

export const MoveAtomModal: React.FC<MoveAtomModalProps> = React.memo(function MoveAtomModal(props) {
    const { selectedAtomsSubject, onStep = () => {}, ...modalProps } = props;
    const { trans } = useAppContext();

    const selectedAtoms = useSubjectState(selectedAtomsSubject);
    const [stepLength, setStepLength] = useState(0.5);

    return (
        <DraggableModal mask={false} {...modalProps} width={380} title={trans(I18N.material3D.translate)} footer={null}>
            <div className={styles.box}>
                <Button
                    type="text"
                    disabled={!selectedAtoms?.length}
                    className={clsx(styles.btn, styles.up)}
                    onClick={() => {
                        const vec = [0, stepLength, 0];
                        onStep(vec);
                    }}
                >
                    <BrmIcon name="caret-up-fill" />
                </Button>
                <Button
                    type="text"
                    disabled={!selectedAtoms?.length}
                    className={clsx(styles.btn, styles.down)}
                    onClick={() => {
                        const vec = [0, -stepLength, 0];
                        onStep(vec);
                    }}
                >
                    <BrmIcon name="caret-down-fill" />
                </Button>
                <Button
                    type="text"
                    disabled={!selectedAtoms?.length}
                    className={clsx(styles.btn, styles.left)}
                    onClick={() => {
                        const vec = [-stepLength, 0, 0];
                        onStep(vec);
                    }}
                >
                    <BrmIcon name="caret-left-fill" />
                </Button>
                <Button
                    type="text"
                    disabled={!selectedAtoms?.length}
                    className={clsx(styles.btn, styles.right)}
                    onClick={() => {
                        const vec = [stepLength, 0, 0];
                        onStep(vec);
                    }}
                >
                    <BrmIcon name="caret-right-fill" />
                </Button>
            </div>
            <div className="flex items-center mt-20">
                <span
                    className="mr-8 text-h6"
                    style={{
                        flexShrink: 0,
                    }}
                >
                    {trans(I18N.material3D.stepLength)}(Å)
                </span>
                <InputNumber
                    className={styles.input}
                    value={stepLength}
                    onChange={v => setStepLength(v || 0)}
                    precision={3}
                    step={0.01}
                    min={0.001}
                    onKeyDown={ev => {
                        ev.stopPropagation();
                    }}
                />
            </div>
        </DraggableModal>
    );
});
