import styles from './Card.module.css';

const Card = (props) => {
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

export default Card;
