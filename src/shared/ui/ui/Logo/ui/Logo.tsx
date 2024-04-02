import { FC } from 'react';
import { Link } from 'react-router-dom';
import LogoImage from '/logo.svg';
import { getDashboardsUrl } from '@/shared/config/url.config';

export const Logo: FC = () => {
	return (
		<Link to={getDashboardsUrl()}>
			<img src={LogoImage} alt="icon logo" />
		</Link>
	);
};
