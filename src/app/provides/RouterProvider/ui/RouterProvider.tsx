import { Loader } from '@/widgets/Loader';
import { FC, ReactElement, Suspense } from 'react';

interface IRouterProviderProps {
	children: ReactElement[] | ReactElement;
}

export const RouterProvider: FC<IRouterProviderProps> = ({ children }) => {
	return <Suspense fallback={<Loader />}>{children}</Suspense>;
};
