module.exports = {
  applicaton: require('./application'),
  authUser: require('./authUser').authUser,
  exportAuthUser: require('./exportAuthUser').exportAuthUser,
  goods: require('./goods'),
  parties: require('./parties'),
  document: require('./document').document,
  goodsToDraft: require('./goodsToDraft'),
  organisation: require('./organisation').organisation,
  headers: require('./headers'),
  userToOrg: require('./userToOrg').userToOrg,
  endUseDetails: require('./endUseDetails'),
  routeOfGoods: require('./routeOfGoods'),
}
