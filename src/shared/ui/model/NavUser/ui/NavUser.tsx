import { FC } from 'react';

import styles from './NavUser.module.scss';

export const NavUser: FC = () => {
	return (
		<div className={styles.user}>
			<div className={styles.avatar}>
				<img src="/navbar/user.svg" alt="Icon user avatar" />
			</div>
			<p>User Name</p>
			<button>
				<img src="/navbar/arrow-bottom.svg" alt="Icon arrow bottom" />
			</button>
		</div>
	);
};
