import { useState, useEffect } from 'react';

import BaseCard from '../components/ui/BaseCard'
import SearchBar from '../components/stock/SearchBar';
import SearchResult from '../components/stock/SearchResult'
import styles from './Home.module.css'

const HomePage = () => {

    const [searchResult, setSearchResult] = useState([]);

    const searchResultHandler = (searchData) => {
        setSearchResult(searchData)
    }

    return (
        <div className={styles.homePage}>
            <div className={styles.homeTitle}>
                <p>Analyze Stock Data</p>
            </div>
            <div className={styles.wrap}>
                <SearchBar onSearchResult={searchResultHandler} />
            </div>
            {searchResult.length > 0 && 
                <SearchResult searchResultData={searchResult} />
            }
        </div>
        
    );
}

export default HomePage;