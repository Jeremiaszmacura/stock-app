import { useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';

import BaseCard from '../components/ui/BaseCard'
import styles from './Company.module.css'
import LoadingSpinner from "../components/ui/LoadingSpinner";


const CompanyPage = () => {

    let today = new Date().toISOString().slice(0, 10)
    const defaultDateFrom = "2018-11-17"
    const defaultDateTo = "2019-11-16"
    const defaultVarHistoricalDays = 300
    const defaultVarHorizonDays = 1
    const defaultPortfloioValue = 1000
    const defaultConfidenceLevel = 99

    const { state } = useLocation();
    const { symbol, name, type, region, marketOpen, marketClose, timezone, currency, matchScore } = state;
    const varRef = useRef(null);
    const [showDate, setShowDate] = useState(false)
    const [dateFrom, setDateFrom] = useState(defaultDateFrom)
    const [dateTo, setDateTo] = useState(defaultDateTo)
    const [plotType, setPlotType] = useState()
    const [companyResultPlot, setCompanyResultPlot] = useState('');
    const [companyHurstExponent, setCompanyHurstExponent] = useState('');
    const [companyHurstPlot, setCompanyHurstPlot] = useState('');
    const [companyResultVar, setCompanyResultVar] = useState('');
    const [selectedInterval, setSelectedInterval] = useState('');
    const [valueAtRisk, setValueAtRisk] = useState('');
    const [hurstExponent, setHurstExponent] = useState('');
    const [varType, setVarType] = useState('');
    const [varHistoricalDays, setVarHistoricalDays] = useState(defaultVarHistoricalDays);
    const [varHorizonDays, setVarHorizonDays] = useState(defaultVarHorizonDays);
    const [varPortfloioValue, setVarPortfloioValue] = useState(defaultPortfloioValue);
    const [varConfidenceLevel, setVarConfidenceLevel] = useState(defaultConfidenceLevel);
    const [companySearchData, setCompanySearchData] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState(false);

    const selectInterval = (event) => {
        setSelectedInterval(event.target.value);
        if(["daily", "weekly", "monthly"].includes(event.target.value)) {
            setShowDate(true)
        } else {
            setShowDate(false)
        }
        if(event.target.value !== "daily") {
            setValueAtRisk('');
            setVarType('');
            varRef.current.style.backgroundColor = "rgba(0, 204, 255, 0.116)";
        }
    }

    const intervalSearchHandler = (event) => {
        setCompanyResultPlot(null);
        setCompanyResultVar(null);
        setErrorMessage(false)
        setIsLoading(true);
        event.preventDefault();
        if (!selectedInterval) {
            setIsLoading(false);
            setErrorMessage("Please select Time Interval");
            return;
        }
        if ( valueAtRisk && !varType) {
            setIsLoading(false);
            setErrorMessage("Please select VaR type");
            return;
        }
        const { symbol, name, type, region, marketOpen, marketClose, timezone, currency, matchScore } = state;
        const CompanySearchData = {
            symbol: String(symbol),
            name: String(name),
            type: String(type),
            region: String(region),
            market_open: String(marketOpen),
            market_close: String(marketClose),
            timezone: String(timezone),
            currency: String(currency),
            interval: String(selectedInterval),
            date_from: String(dateFrom),
            date_to: String(dateTo),
            plot_type: String(plotType),
            calculate: [valueAtRisk, hurstExponent],
            var_type: String(varType),
            portfolio_value: Number(varPortfloioValue),
            confidence_level: Number(varConfidenceLevel/100),
            historical_days: Number(varHistoricalDays),
            horizon_days: Number(varHorizonDays),
        }
        console.log(CompanySearchData)
        setCompanySearchData(CompanySearchData)
        fetch(
            'http://localhost:8000/stock-data/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': "Bearer " + localStorage.getItem('tokenInStorage'),
                },
                body: JSON.stringify(CompanySearchData)
            }
        )
        .then(res => {
            if (res.ok) {
                console.log('[CLIENT] fetch successful');
            } else {
                console.log('[CLIENT] fetch NOT successful');
            }
            res.json().then((data) => {
                data = JSON.parse(data)
                setIsLoading(false);
                setCompanyResultPlot(data['plot']);
                if(data['var']) {
                    setCompanyResultVar(data['var'].toFixed(2));
                    setVarHistoricalDays(data['historical_days']);
                    console.log(data['historical_days'])
                }
                if(data['hurst_exponent']) {
                    setCompanyHurstExponent(data['hurst_exponent'].toFixed(4));
                    setCompanyHurstPlot(data['hurst_plot']);
                }
            });
        }).catch(err => {
            console.log(err);
            setIsLoading(false);
        });
    }

    const handleChangeVAR = (event) => {
        if(selectedInterval !== "daily") {
            setErrorMessage("Value at risk can only be calculated for the daily time interval");
            return;
        } else {
            setErrorMessage('');
        }
        if(valueAtRisk) {
            setValueAtRisk('');
            setVarType('');
            event.target.style.backgroundColor = 'rgba(0, 204, 255, 0.116)';
        }
        else {
            event.target.style.backgroundColor = 'rgba(0, 204, 255, 0.719)';
            setValueAtRisk(event.target.value);
        }
    }

    const handleChangeHurst = (event) => {
        if(hurstExponent) {
            setHurstExponent('')
            event.target.style.backgroundColor = 'rgba(0, 204, 255, 0.116)';
        }
        else {
            event.target.style.backgroundColor = 'rgba(0, 204, 255, 0.719)';
            setHurstExponent(event.target.value)
        }
    }

    return (
        <div className={styles.companyPage}>
            <div className={styles.companyOptions}>
            <div className={styles.overBaseCard}>
                <BaseCard>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Symbol:</p>
                        <p className={styles.pVariable}>{symbol}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Name:</p>
                        <p className={styles.pVariable}>{name}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Type:</p>
                        <p className={styles.pVariable}>{type}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Region:</p>
                        <p className={styles.pVariable}>{region}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Market Open:</p>
                        <p className={styles.pVariable}>{marketOpen}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Market Close:</p>
                        <p className={styles.pVariable}>{marketClose}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Timezone:</p>
                        <p className={styles.pVariable}>{timezone}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Currency:</p>
                        <p className={styles.pVariable}>{currency}</p>
                    </div>
                    <div className={styles.contentRow}>
                        <p className={styles.pTitle}>Match Score:</p>
                        <p className={styles.pVariable}>{matchScore}</p>
                    </div>
                </BaseCard>
            </div>
            <div className={styles.analyzeCompany}>
                <div className={styles.customSelect}>
                    <select onChange={selectInterval} defaultValue={''}>
                        <option hidden value="" disabled>Time Interval</option>
                        <option value="1min">1min</option>
                        <option value="5min">5min</option>
                        <option value="15min">15min</option>
                        <option value="30min">30min</option>
                        <option value="60min">60min</option>
                        <option value="daily">daily</option>
                        <option value="weekly">weekly</option>
                        <option value="monthly">monthly</option>
                    </select>
                    <select onChange={e => setPlotType(e.target.value)} defaultValue={''}>
                        <option hidden value="" disabled>Plot Type</option>
                        <option value="linear">linear</option>
                        <option value="candlestick">candlestick</option>
                    </select>
                </div>
                {showDate && <div className={styles.dateInput}>
                    <div className={styles.dateInputUnit}>
                        <label htmlFor='varHistoricalDays'>Date from</label>
                        <input type="date" id="start" name="date-begin" min="1900-01-02" defaultValue={defaultDateFrom} onChange={e => setDateFrom(e.target.value)}/>
                    </div>
                    <div className={styles.dateInputUnit}>
                        <label htmlFor='varHistoricalDays'>Date to</label>
                        <input type="date" id="start" name="date-end" min="1900-01-01" defaultValue={defaultDateTo} onChange={e => setDateTo(e.target.value)}/>
                    </div>
                </div> }
                <div className={styles.multiSelect}>
                    <div className={styles.multiSelectBox}>
                        <button id={styles.var} ref={varRef} onClick={handleChangeVAR} value="var">Value at Risk</button>
                    </div>
                    <div className={styles.multiSelectBox}>
                        <button id={styles.hurst} onClick={handleChangeHurst} value="hurst">Hurst Exponent</button>
                    </div>
                </div>
                { valueAtRisk &&
                <div>
                    <div className={styles.customSelect}>
                        <select onChange={e => setVarType(e.target.value)} defaultValue={''}>
                            <option hidden value="" disabled>VaR type</option>
                            <option value="historical">historical simulation</option>
                            <option value="linear_model">linear model simulation</option>
                            <option value="monte_carlo">monte carlo simulation</option>
                        </select>
                    </div>
                    <div className={styles.customInputSection}>
                        <div className={styles.customInput}>
                            <label htmlFor='varHistoricalDays'>VaR historical days</label>
                            <input type='number' min="10" max="10000" defaultValue={defaultVarHistoricalDays} onChange={e => setVarHistoricalDays(e.target.value)} required id='varHistoricalDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>VaR horizon in days</label>
                            <input type='number' min="10" max="10000" defaultValue={defaultVarHorizonDays} onChange={e => setVarHorizonDays(e.target.value)} required id='varHorizonDays' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>Portfolio value</label>
                            <input type='number' min="10" max="1000000000" defaultValue={defaultPortfloioValue} onChange={e => setVarPortfloioValue(e.target.value)} required id='varPortfloioValue' />
                        </div>
                        <div className={styles.customInput}>
                            <label htmlFor='varHorizonDays'>Confidence level %</label>
                            <input type='number' min="1" max="99" defaultValue={defaultConfidenceLevel} onChange={e => setVarConfidenceLevel(e.target.value)} required id='varConfidenceLevel' />
                        </div>
                    </div>
                </div>
                }
                <div id={styles.selectButton}>
                    <button onClick={intervalSearchHandler}>Select</button>
                </div>
            </div>
            </div>
            { isLoading && <LoadingSpinner /> }
            { errorMessage &&
            <div className={styles.errorMessageContainer}>
                <p>{errorMessage}</p>
            </div>
            }
            {companyResultVar &&
                <div className={styles.varResult}>
                    <BaseCard>
                        <div className={styles.varResultParameters}>
                            <p>Portfolio value:</p>
                            <p>VaR method:</p>
                            <p>Confidence level:</p>
                            <p>Historical days:</p>
                            <p>Time horizon:</p>
                            <p>{companySearchData.portfolio_value}</p>
                            <p>{companySearchData.var_type}</p>
                            <p>{companySearchData.confidence_level*100}%</p>
                            <p>{varHistoricalDays}</p>
                            <p>{companySearchData.horizon_days} days</p>
                        </div>
                        <p id={styles.varValue}> Value at Risk: {companyResultVar} </p>
                    </BaseCard>
                </div>
            }
            {companyHurstExponent &&
                <div className={styles.varResult}>
                <BaseCard>
                    <p id={styles.varValue}> Hurst Exponent: {companyHurstExponent} </p>
                </BaseCard>
            </div>
            }
            {companyHurstPlot &&
                <div>
                    <div className={styles.plot}>
                        <div className={styles.plotBox}>
                            <img src={`data:image/png;base64,${companyHurstPlot}`} alt='Plot'/>
                        </div>
                    </div>
                </div>
            }
            {companyResultPlot &&
                <div>
                    <div className={styles.plot}>
                        <div className={styles.plotBox}>
                            <img src={`data:image/png;base64,${companyResultPlot}`} alt='Plot'/>
                        </div>
                    </div>
                </div>
            }
        </div>

    );
}

export default CompanyPage;
