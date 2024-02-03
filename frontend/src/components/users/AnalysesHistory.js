import styles from './AnalysesHistory.module.css';
import AnalysesHistoryUnit from './AnalysesHistoryUnit';

const AnalysesHistory = (props) => {

    console.log(props.analysesHistoryData)
    console.log(typeof(props.analysesHistoryData))

    // useEffect(() => {
    //     for(var i in json_data)
    //     result.push([i, json_data [i]]);
    // }, [])

    return (
        <ul className={styles.list}>
            {props.analysesHistoryData.map((analysed, id) => (
                // <div><p>hi</p></div>
                <AnalysesHistoryUnit
                key={id}
                symbol={analysed.symbol}
                name={analysed.name}
                type={analysed.type}
                region={analysed.region}
                marketOpen={analysed.marketOpen}
                marketClose={analysed.marketClose}
                timezone={analysed.timezone}
                currency={analysed.currency}
                matchScore={analysed.matchScore}
                />
            ))}
        </ul>
    );
}

export default AnalysesHistory;
