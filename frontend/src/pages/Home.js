import { useState } from 'react';

import SearchBar from '../components/stock/SearchBar';
import SearchResult from '../components/stock/SearchResult'
import styles from './Home.module.css'

const HomePage = () => {

    const [searchResult, setSearchResult] = useState([]);
    const [searchNotFound, setSearchNotFound] = useState('')

    const searchResultHandler = (searchData) => {
        setSearchResult(searchData)
        if (searchData.message) {
            console.log("hihi")
            setSearchNotFound(searchData.message)
        }
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
            {searchNotFound.length > 0 &&
                <div className={styles.searchNotFound}>
                    <p>{searchNotFound}</p>
                </div>
            }
        </div>
        
    );
}

export default HomePage;