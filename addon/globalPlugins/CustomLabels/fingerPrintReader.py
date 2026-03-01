# fingerPrintReader
# A part of Custom Labels addon for NVDA
# The addon Allows users to assign custom labels to unlabeled controls and edit and manage them.
# copyright: 2026 Kefas Lungu
# This file is licensed under the GNU General Public License v2.
# See the file COPYING.txt for details.
# This module provides functions to generate a stable fingerprint for an NVDAObject based on its properties.

from NVDAObjects.UIA import UIA


def getObjectFingerprint(obj):
	"""
	Return a stable fingerprint for an NVDAObject.
	Uses backend-specific properties plus the original name for differentiation.
	"""
	try:
		fp = {}

		# App name
		try:
			fp["app"] = obj.appModule.appName
		except Exception:
			fp["app"] = "unknown"

		# Role
		try:
			fp["role"] = int(obj.role)
		except Exception:
			fp["role"] = 0

		# Original name - helps differentiate controls with different names
		# (e.g., labeled buttons vs unlabeled ones in the same app)
		# Use _get_name() to bypass any custom label overlay and get the real name
		try:
			if hasattr(obj, '_get_name'):
				fp["name"] = obj._get_name() or ""
			else:
				fp["name"] = obj.name or ""
		except Exception:
			fp["name"] = ""

		# Description - helps differentiate controls with the same name
		# (e.g., multiple "Filter Options" buttons in Java apps like Ghidra)
		try:
			fp["description"] = obj.description or ""
		except Exception:
			fp["description"] = ""

		# Parent name - helps differentiate controls in different
		# toolbars/panels that otherwise have identical properties
		try:
			parent = obj.parent
			fp["parentName"] = parent.name or "" if parent else ""
		except Exception:
			fp["parentName"] = ""

		# Backend-specific ID
		if isinstance(obj, UIA):
			fp["backend"] = "UIA"
			try:
				fp["automationId"] = obj.UIAElement.currentAutomationId or ""
			except Exception:
				fp["automationId"] = ""
			try:
				fp["className"] = obj.windowClassName or ""
			except Exception:
				fp["className"] = ""
		else:
			# IA2 - covers both native desktop apps and web content (IA2Web)
			# windowClassName and windowControlID are always available
			# name (set above) provides differentiation between controls
			fp["backend"] = "IA2"
			try:
				fp["windowClassName"] = obj.windowClassName or ""
			except Exception:
				fp["windowClassName"] = ""
			try:
				fp["windowControlID"] = obj.windowControlID or 0
			except Exception:
				fp["windowControlID"] = 0

		# Convert to hashable tuple
		return tuple(sorted(fp.items()))

	except Exception:
		return None


def fingerprintToDict(fp):
	"""Convert a fingerprint tuple back to a dict."""
	if fp:
		return dict(fp)
	return {}
