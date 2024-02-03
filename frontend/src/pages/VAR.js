import BaseCard from '../components/ui/BaseCard'
import styles from './VAR.module.css'

const VARPage = () => {

    return (
        <div className={styles.aboutVaR}>
            <BaseCard>
                <p className={styles.varTitle}>Value at Risk</p>
                <div className={styles.varContent}>
                    <p>Value at Risk is measure that allows to specify the investment risk in the form of a numerical value.</p>
                    <br />
                    <p>In other words we can say:</p>
                    <p id={styles.varQuote}>I am X percent certain there will not be a loss of more than V dollars in the next N days.</p>
                    <br />
                    <p>The variable V is the VaR of the portfolio. It is a function of two parameters: the time
horizon (N days) and the confidence level (X%). It is the loss level over N days that has
a probability of only (100-X)% of being exceeded.</p>
                    <br />
                </div>
            </BaseCard>
            <BaseCard>
                <p className={styles.varTitle}>Historical Simulation</p>
                <div className={styles.varContent}>
                    <p>It involves using past data as a guide to what will happen in the future</p>
                </div>
            </BaseCard>
            <BaseCard>
                <p className={styles.varTitle}>Linear Model Simulation</p>
                <div className={styles.varContent}>
                    <p>Uses mean, standard deviation of historical data to calculate VaR</p>
                </div>
            </BaseCard>
            <BaseCard>
                <p className={styles.varTitle}>Monte Carlo Simulation</p>
                <div className={styles.varContent}>
                    <p>description...</p>
                </div>
            </BaseCard>
        </div>
    );
}

export default VARPage;
