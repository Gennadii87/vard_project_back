import { FC } from 'react';

import styles from './Loader.module.scss';

import cn from '@/shared/lib/classNames';

export const Loader: FC = () => {
	return (
		<div className={styles.loader}>
			<div className={cn(styles['jimu-primary-loading'], {}, [styles['justify-content-center']])}></div>
		</div>
	);
};
