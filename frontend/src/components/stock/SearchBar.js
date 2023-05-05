
import { useState } from 'react';
import 'font-awesome/css/font-awesome.min.css';

import LoadingSpinner from "../ui/LoadingSpinner";
import styles from './SearchBar.module.css'

const SearchBar = (props) => {

    const [searchInput, setSearchInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            searchHandler(event)
        }
    }

    const handleChange = (event) => {
        event.preventDefault();
        setSearchInput(event.target.value);
      };
    
    const searchHandler = (event) => {
        event.preventDefault();
        if (!searchInput) {
            return
        }
        setIsLoading(true);
        fetch(
            'http://localhost:8000/stock-data/search?' + new URLSearchParams({
                symbol: searchInput,
            }),
            {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                },
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] login - fetch successful');
            } else {
                console.log('[CLIENT] login - fetch NOT successful');
            }
            res.json().then((data) => {
                setIsLoading(false);
                props.onSearchResult(data);
            });
        }).catch(err => {
            setIsLoading(false);
            console.log(err);
        });
    }

    return (
        <div>
            <div className={styles.search}>
                <input
                    className={styles.searchTerm}
                    type="text"
                    placeholder="Company Name"
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    value={searchInput} />
                <button type="submit" className={styles.searchButton} onClick={searchHandler}>
                    <i className="fa fa-search"></i>
                </button>
            </div>
            { isLoading && <LoadingSpinner /> }
        </div>
);
}

export default SearchBar;