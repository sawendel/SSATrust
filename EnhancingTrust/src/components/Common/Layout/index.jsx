import { Outlet } from "react-router-dom";
import { Helmet } from "react-helmet";
import { useQuery } from '../../../hooks';

const Layout = () => {
  const query = useQuery();
  return (
    <>
      <Helmet>
        <title>{query?.get('title') || 'CFS Research on Trust and Scams'}</title>
      </Helmet>
      <Outlet />
    </>
  );
}

export default Layout;
