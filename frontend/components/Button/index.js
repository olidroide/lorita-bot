import styles from '../../styles/Button.module.css'

export default function Button({children, onClick}) {
    return (
        <>
            <button onClick={onClick} className={styles.button}>
                {children}
            </button>
        </>
    )
}