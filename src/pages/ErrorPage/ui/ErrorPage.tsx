import { FC } from 'react';
import { useNavigate } from 'react-router-dom';

export const ErrorPage: FC = () => {
	const navigate = useNavigate();

	return (
		<div
			style={{
				minHeight: '100vh',
				display: 'flex',
				justifyContent: 'center',
				alignItems: 'center',
				flexDirection: 'column',
				rowGap: '25px',
				backgroundColor: 'black',
				color: 'white',
				fontSize: '50px',
			}}
		>
			<div>Oops, something went wrong!</div>
			<button onClick={() => navigate('/')}>Go home</button>
		</div>
	);
};
