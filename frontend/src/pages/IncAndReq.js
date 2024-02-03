import { useRef } from 'react';

import BaseCard from '../components/ui/BaseCard'
import styles from './IncAndReqPage.module.css'

const IncAndReqPage = () => {

    const incTitleInputRef = useRef();
    const incDescriptionInputRef = useRef();
    const reqTitleInputRef = useRef();
    const reqDescriptionInputRef = useRef();

    const submitHandler = () => {
        console.log("Submit")
    }
    return (
        <div className={styles.incAndReqPage}>
            <BaseCard>
                <form className={styles.form} onSubmit={submitHandler}>
                    <h1 className={styles.heading}>Incident</h1>
                    <div className={styles.control}>
                        <label htmlFor='title'>Title</label>
                        <input type='text' required id='title' ref={incTitleInputRef} />
                    </div>
                    <div className={styles.control}>
                        <label htmlFor='description'>Description</label>
                        <textarea rows="5" type='text' required id='description' ref={incDescriptionInputRef} />
                    </div>
                    <div className={styles.actions}>
                        <button>Send</button>
                    </div>
                </form>
            </BaseCard>
            <BaseCard>
                <form className={styles.form} onSubmit={submitHandler}>
                    <h1 className={styles.heading}>Request</h1>
                    <div className={styles.control}>
                        <label htmlFor='title'>Title</label>
                        <input type='text' required id='title' ref={reqTitleInputRef} />
                    </div>
                    <div className={styles.control}>
                        <label htmlFor='description'>Description</label>
                        <textarea rows="5" type='text' required id='description' ref={reqDescriptionInputRef} />
                    </div>
                    <div className={styles.actions}>
                        <button>Send</button>
                    </div>
                </form>
            </BaseCard>
        </div>
    );
}

export default IncAndReqPage;
