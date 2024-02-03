import styles from './SearchResult.module.css';
import SearchResultUnit from './SearchResultUnit';

const SearchResult = (props) => {

    return (
        <ul className={styles.list}>
            {props.searchResultData.map((company, id) => (
                <SearchResultUnit
                key={id}
                symbol={company.symbol}
                name={company.name}
                type={company.type}
                region={company.region}
                marketOpen={company.marketOpen}
                marketClose={company.marketClose}
                timezone={company.timezone}
                currency={company.currency}
                matchScore={company.matchScore}
                />
            ))}
        </ul>
    );
}

export default SearchResult;
