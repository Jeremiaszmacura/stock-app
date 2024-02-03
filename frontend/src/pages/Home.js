import { useState, useContext } from 'react';

import SearchBar from '../components/stock/SearchBar';
import SearchResult from '../components/stock/SearchResult'
import { UserContext, AdminContext } from '../UserContext';
import { logout } from '../tests/logout.js'
import styles from './Home.module.css'

const HomePage = () => {

    const { user, setUser } = useContext(UserContext);
    // eslint-disable-next-line no-unused-vars
    const { admin, setAdmin } = useContext(AdminContext);

    const [searchResult, setSearchResult] = useState([]);
    const [searchNotFound, setSearchNotFound] = useState('')

    const searchResultHandler = (searchData) => {
        setSearchResult(searchData["data"])
        console.log(searchData["user_availability"])
        if(searchData["user_availability"] === false) {
            setUser(null);
            setAdmin(null);
        }
        if(searchData.detail == "Could not validate credentials") {
            console.log("xD");
            setSearchNotFound("Your session has expired, please login again");
            logout();
            setUser(null);
            setAdmin(null);
        }
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
            {searchResult && searchResult.length > 0 &&
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
