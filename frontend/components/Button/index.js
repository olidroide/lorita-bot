import styles from '../../styles/Button.module.css'

export default function Button({children, onClick, color}) {
    const colors = {
        telegram: styles.telegram,
        whatsapp: styles.whatsapp,
    }
    
    return (
        <>
            <button onClick={onClick} className={`${styles.button} ${colors[color]}`}>
                {children}
            </button>
        </>
    )
}


// PROPTYPES REACT
// Button.propTypes = {
//  color: propTypes.oneOf([])
// };
