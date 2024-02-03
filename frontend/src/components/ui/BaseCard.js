import styles from './BaseCard.module.css';

const BaseCard = (props) => {
    return (
        <div className={styles.body}>
            <div className={styles.box}>
                <div className={styles.glass}></div>
                <div className={styles.content}>
                    {props.children}
                </div>
            </div>
        </div>
    );
}

export default BaseCard;
