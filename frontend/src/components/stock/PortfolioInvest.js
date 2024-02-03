import styles from './PortfolioInvest.module.css';
import { Trash } from 'react-bootstrap-icons'
// import YourSvg from "../../public/trash.svg";

const PortfolioInvest = (props) => {

    const removeFromPortfolio = (companySymbol, companyInvestList) => {
        delete companyInvestList[companySymbol]
        // return companyInvestList => [...props.companyInvestList, companyAdded]
        // console.log("hi")
        // console.log(companyInvestList.lenght)
        return companyInvestList
        // let companyAdded = {
        //     companyInvestSymbol: companyInvestSymbol,
        //     companyInvestValue: companyInvestValue
        // }
        // setCompanyInvestList(companyInvestList => [...companyInvestList, companyAdded])
        // console.log(companyInvestList)
    }

    return (
        <div className={styles.box}>
            <div className={styles.investItem}>
                <p>Company Symbol:</p>
                <p>{props.companySymbol}</p>
                <p>Value: {props.companyValue}</p>
                {/* <img className={styles.trash} src={YourSvg} alt="Your SVG" /> */}
                {/* <button className={styles.trashButton}> */}
                    <span onClick={() => removeFromPortfolio(props.companySymbol, props.companyInvestList)} className={styles.trashChangeColor}>
                        <Trash size={20} />
                    </span>
                {/* </button> */}

            </div>
        </div>
    );
}

export default PortfolioInvest;
