"""
Material-specific fire safety logic.
"""

# TODO: Implement Section 603 (Combustible Material in Types I and II Construction).
# Implementation of Section 603 is currently deferred.
# It contains a highly granular list of exceptions (e.g., thermal insulation, millwork,
# roof coverings) and delegates to many other chapters (like Chapter 8 for interior
# finishes, Chapter 15 for roofs, and Chapter 26 for plastics).
# Future implementations will require robust element-level metadata from the BIM model
# (e.g., flame spread indices, material taxonomy) to validate these exceptions.
