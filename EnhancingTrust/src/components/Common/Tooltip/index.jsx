import Tooltip from 'rc-tooltip';

const CommonTooltip = ({ children, text, show, placement = "top" }) => !!text?.length ? (
  <Tooltip placement={placement} visible={show} overlay={<><i className="et-warning" /> <span dangerouslySetInnerHTML={{ __html: '<span>' + text + '</span> ' }} /> </>}>
    {children}
  </Tooltip>
) : children;

export default CommonTooltip;
